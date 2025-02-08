import os
import redis
from datetime import timedelta
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from elasticsearch import Elasticsearch

app = Flask(__name__)
CORS(app)

load_dotenv()
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')
db_uri = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
redis_host = os.getenv('REDIS_HOST')
redis_port = os.getenv('REDIS_PORT')
elasticsearch_host = os.getenv('ELASTICSEARCH_HOST')
elasticsearch_port = os.getenv('ELASTICSEARCH_PORT')

app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=5)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(hours=30)
#app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=15)
#app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(seconds=30)
app.config['ELASTICSEARCH_URL'] = f"http://{elasticsearch_host}:{elasticsearch_port}"

db = SQLAlchemy(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
r = redis.StrictRedis(host=redis_host, port=redis_port, db=0, decode_responses=True)
app.es = Elasticsearch([app.config['ELASTICSEARCH_URL']])