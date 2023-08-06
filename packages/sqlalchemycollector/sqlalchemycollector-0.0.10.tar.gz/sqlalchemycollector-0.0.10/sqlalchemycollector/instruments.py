from __future__ import absolute_import, division, print_function, unicode_literals

import os

from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.trace import TracerProvider, ReadableSpan
from opentelemetry.sdk.trace.export import SpanExporter, SpanExportResult, SimpleSpanProcessor
from opentelemetry import trace

from datetime import datetime

from opentelemetry.semconv.trace import SpanAttributes
from six import string_types

import typing

import json

import uuid

from opentelemetry.trace import Status, StatusCode
from sqlalchemy.event import listen

FILE_NAME = 'metis-log-collector.log'

METIS_REQUEST_SPAN_ATTRIBUTE_IDENTIFIER = 'track.by.metis'
METIS_QUERY_SPAN_NAME = 'metis-query'


def add_quote_to_value_of_type_string(value):
    if isinstance(value, string_types):
        new_value = str(value).replace("'", "''")
        return "'{}'".format(new_value)
    return value


def fix_sql_query(sql, params):
    """without the fix the query is not working because string is not quoted"""
    fixed_param = {key: add_quote_to_value_of_type_string(value) for key, value in params.items()}
    return sql % fixed_param


def _normalize_vendor(vendor):
    """Return a canonical name for a type of database."""
    if not vendor:
        return "db"  # should this ever happen?

    if "sqlite" in vendor:
        return "sqlite"

    if "postgres" in vendor or vendor == "psycopg2":
        return "postgresql"

    return vendor


class MetisExporter(SpanExporter):

    def __init__(
            self,
            filename,
    ):
        self.dict = {}
        self.filename = filename

    def export(self, spans: typing.Sequence[ReadableSpan]) -> SpanExportResult:
        for span in spans:
            trace_id = span.context.trace_id

            if self.dict.get(trace_id) is None:
                self.dict[trace_id] = []

            self.dict[trace_id].append(span)

            if span.parent is None:
                self.export_to_file(trace_id)

        return SpanExportResult.SUCCESS

    def export_to_file(self, trace_id):
        spans = self.dict[trace_id]
        del self.dict[trace_id]

        parent = next(x for x in spans if x.attributes.get(METIS_REQUEST_SPAN_ATTRIBUTE_IDENTIFIER))

        # for now, we don't track sql queries that not under request span
        if not parent:
            return

        spans.remove(parent)

        metis_spans = list(filter(lambda x: x.name == METIS_QUERY_SPAN_NAME, spans))

        if not len(metis_spans):
            return

        data = {
            'logs': list(map(lambda x: {
                '_uuid': str(uuid.uuid1()),
                'query': x.attributes.get(SpanAttributes.DB_STATEMENT),
                'dbEngine': x.attributes.get(SpanAttributes.DB_SYSTEM),
                'date': datetime.utcnow().isoformat(),
            }, metis_spans)),
            'framework': 'Flask',
            'path': parent.attributes.get(SpanAttributes.HTTP_TARGET, 'N/A'),
            'operationType': parent.attributes.get(SpanAttributes.HTTP_METHOD, 'N/A'),
            'requestDuration': (parent.end_time - parent.start_time) / 1000000,
            'requestStatus': parent.attributes.get(SpanAttributes.HTTP_STATUS_CODE, 'N/A')
        }

        with open(self.filename, 'a') as file:
            file.write(json.dumps(data) + '\n')


def collect_logs(app, engine, file_name=FILE_NAME):
    filename = os.getenv('METIS_LOG_FILE_NAME', file_name)

    metis = MetisInstrumentor(filename)
    metis.instrument_app(app, engine)


class MetisInstrumentor:
    def __init__(self, filename):
        self.tracer_provider = TracerProvider()
        self.processor = SimpleSpanProcessor(MetisExporter(filename))
        self.tracer_provider.add_span_processor(self.processor)
        self.tracer = trace.get_tracer(
            'metis',
            '',
            tracer_provider=self.tracer_provider,
        )

    def instrument_app(self, app, engine):
        def request_hook(span, flask_request_environ):
            span.set_attribute(METIS_REQUEST_SPAN_ATTRIBUTE_IDENTIFIER, True)

        def response_hook(span, status, response_headers):
            pass

        FlaskInstrumentor().instrument_app(app, tracer_provider=self.tracer_provider,
                                           request_hook=request_hook,
                                           response_hook=response_hook)

        RequestsInstrumentor().instrument()

        db_vendor = _normalize_vendor(engine.name)

        def before_query_hook(conn, cursor, statement, parameters, context, executemany):
            span = self.tracer.start_span(METIS_QUERY_SPAN_NAME, kind=trace.SpanKind.CLIENT)

            interpolated_statement = fix_sql_query(statement, parameters)

            span.set_attribute(SpanAttributes.DB_SYSTEM, db_vendor)

            span.set_attribute(SpanAttributes.DB_STATEMENT, interpolated_statement)

            context._otel_span = span
            return statement, parameters

        listen(engine, "before_cursor_execute", before_query_hook, retval=True)

        def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
            span = getattr(context, "_otel_span", None)
            if span is None:
                return

            span.end()

        listen(engine, "after_cursor_execute", after_cursor_execute)

        def handle_error(conn, cursor, error, context):
            span = getattr(context.execution_context, "_otel_span", None)
            if span is None:
                return

            if span.is_recording():
                span.set_status(
                    Status(
                        StatusCode.ERROR,
                        str(context.original_exception),
                    )
                )
            span.end()

        listen(engine, "handle_error", handle_error)
