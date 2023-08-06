# Metis Flask SQLAlchemy log collector

This library collects http requests and sql queries in Flask & SQLalchemy 
application and stores them in a local log file.

The log can be analyzed using a [Visual Studio Code extension](https://marketplace.visualstudio.com/items?itemName=Metis.dba-ai-vscode)

This library uses [OpenTelemetry](https://pypi.org/project/opentelemetry-sdk/) to instrument both Flask and SQLAlchemy.

Tested on python 3.8.9, Flask 2.1.1, SQLAlchemy 1.4.33


## How to use the log collector in your application

```bash
pip install sqlalchemycollector
```

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemycollector import collect_logs

# existing app initialization
app = Flask()
db = SQLAlchemy(app)

# optionally, you can pass a log file name, or we will use our default file name 'metis-log-collector.json
optional_log_file_name = 'my-metis-logs.log'

# add the following line to start collect logs for metis
collect_logs(app, db.get_engine(), optional_log_file_name)
```

### Example of a log entry (might be changed in the future) 
```json
{
  "logs": [
    {
      "_uuid": "da9f502a-b328-11ec-ae45-b276246b1dca",
      "query": "SELECT booking.book.title AS booking_book_title \nFROM booking.book",
      "dbEngine": "postgresql",
      "date": "2022-04-03T08:34:18.958128"
    }
  ],
  "framework": "Flask",
  "path": "/books",
  "operationType": "GET",
  "requestDuration": 1132.736,
  "requestStatus": 200
}
```
