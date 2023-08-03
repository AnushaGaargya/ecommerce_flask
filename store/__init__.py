import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


# basedir = os.path.abspath(os.path.dirname(__file__))
file_path = os.path.abspath(os.getcwd())+"/store/test.db"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + file_path
app.config['SECRET_KEY']= 'abcde'
app.config['UPLOAD_FOLDER'] = 'static'
# app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images')
# photos = UploadSet('photos', IMAGES)


db  = SQLAlchemy(app) 
app.app_context().push()
bcrypt = Bcrypt(app)

from store.admin import routes
from store.products import routes