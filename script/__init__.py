from flask import Flask
import os
from script.config import DevelopmentConfig, TestingConfig

def create_app(test_config=None):
    app = Flask(__name__, template_folder='../templates/', static_folder='../static/', instance_relative_config=True)

    if test_config is None:
        # load the instance of development config, when not testing
        app.config.from_object(DevelopmentConfig())
    else:
        # load the default test config and then load passed in test config
        app.config.from_object(TestingConfig())
        app.config.from_mapping(test_config)
    
    from script.models import db
    db.init_app(app)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    

    return app