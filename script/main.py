from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__, template_folder='../templates/', static_folder='../static/')

app.config['SECRET_KEY'] = 'ThisK3Y$SECRET_KEY'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../budget_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

import routes