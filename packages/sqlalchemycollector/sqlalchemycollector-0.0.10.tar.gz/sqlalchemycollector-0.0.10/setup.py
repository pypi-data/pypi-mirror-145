from setuptools import setup, find_packages
from pathlib import Path


VERSION = '0.0.10'
this_directory = Path(__file__).parent
long_description = (this_directory / "README-public.md").read_text()

setup(
    name='sqlalchemycollector',
    version=VERSION,
    author='Metis dev',
    author_email='devops@metisdata.io',
    description='Metis log collector for Flask and SQLAlchemy',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/metis-data/sqlalchemy_collector',
    project_urls = {
        "Bug Tracker": "https://github.com/metis-data/sqlalchemy_collector/issues"
    },
    license='',
    packages=['sqlalchemycollector'],
    install_requires=['opentelemetry-api', 'opentelemetry-sdk', 'sqlalchemy', 'flask', 'requests', 'six', 'opentelemetry-instrumentation-sqlalchemy', 'opentelemetry-instrumentation-flask', 'opentelemetry-instrumentation-requests'],
)
