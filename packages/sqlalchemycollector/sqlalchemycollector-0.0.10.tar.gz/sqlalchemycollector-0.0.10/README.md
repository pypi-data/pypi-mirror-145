# Metis Flask SQLAlchemy instumentation

## how to instrument 


```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemycollector import instrument_sqlalchemy

app = Flask()
db = SQLAlchemy(app)

# add the following line to instrument SQLAlchemy
instrument_sqlalchemy(app, db.get_engine())
```


## to build the package

```shell
# in the root of the project run the following command
python3 setup.py sdist bdist_wheel

# to install the package from local folder
python3 -m pip install ~/<path-to-root-folder>/dist/sqlalchemycollector-0.0.1.tar.gz
```


## to run demo app
```shell
cd ./demo-app
python3 -m venv venv
pip install -r requirements.txt
python bookmanager.py
```
