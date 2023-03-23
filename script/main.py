from . import create_app
from flask_login import LoginManager

app = create_app()

login_manager = LoginManager(app)
login_manager.login_view = 'login'


import script.routes