import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_msearch import Search

# from werkzeug.utils import secure_filename


# basedir = os.path.abspath(os.path.dirname(__file__))
file_path = os.path.abspath(os.getcwd())+"/store/test.db"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + file_path
app.config['SECRET_KEY']= 'abcde'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
# app.config['UPLOAD_FOLDER']  = os.path.join(basedir, 'static/images')

db  = SQLAlchemy(app)
app.app_context().push()


bcrypt = Bcrypt(app)
search1 = Search()
search1.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view="customerLogin"
login_manager.needs_refresh_message_category="danger"
login_manager.login_message = u"Please login first"


from store.admin import routes
from store.products import routes
from store.carts import routes
from store.customer import routes