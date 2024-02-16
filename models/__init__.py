from flask import Flask
import secrets
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__, template_folder='templates')
secret_key = secrets.token_hex(16)
app.config['SECRET_KEY'] = secret_key

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db' 

db = SQLAlchemy(app)
bcrypt= Bcrypt(app)
login_manager = LoginManager(app)

from models import routes