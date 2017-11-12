import sqlalchemy
from bottle import Bottle, TEMPLATE_PATH, response, request
from sqlalchemy import create_engine
from bottle.ext import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Bottle()
Base = declarative_base()
engine = create_engine('sqlite:///megasena.db', echo=True)
create_session = sessionmaker(bind=engine)
TEMPLATE_PATH.insert(0, 'app/views/')
plugin = sqlalchemy.Plugin(engine, Base.metadata, keyword='db', create=True, commit=True, use_kwargs=False)
app.install(plugin)

from app.sorterio_controller import *

@app.hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = request.environ.get('HTTP_ORIGIN')
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Authorization, Origin, Accept, Content-Type, X-Requested-With'

@app.route('/', method = 'OPTIONS')
@app.route('/<path:path>', method = 'OPTIONS')
def options_handler(path = None):
    return
