# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data. 
CSRF_SESSION_KEY = "secret"

STATIC_IMAGE_PATH = BASE_DIR+"/hairstylist/static/img/"
TRAIN_DATA = BASE_DIR+'/hairstylist/traindata/'

# Secret key for signing cookies
SECRET_KEY      = "secret"
