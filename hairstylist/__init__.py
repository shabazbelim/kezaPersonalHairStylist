from flask import Flask
from config import *
from flask_cors import CORS

app = Flask(__name__,static_folder='static', static_url_path='')

app.config.from_object('config')

CORS(app)


from hairstylist.api.controllers import *