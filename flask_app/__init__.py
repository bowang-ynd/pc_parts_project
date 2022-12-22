from flask import Flask
from flask_bcrypt import Bcrypt

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

UPLOAD_FOLDER = './flask_app/static/uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
DATABASE = 'old_egg_schema'

# set up app
app = Flask(__name__)
app.secret_key = "this is a very secret key for ynd projects"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# set up bcrypt
bcrypt = Bcrypt(app)
