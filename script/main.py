from . import create_app
from script.routes import general

app = create_app()

app.register_blueprint(general)