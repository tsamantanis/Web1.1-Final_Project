from flask import Flask
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/kanbanCalendar') + "?retryWrites=false"
app.config["MONGO_URI"] = host
mongo = PyMongo(app)
database = mongo.db
