from flask import Flask
import os

    

def create_app(test_config=None):
    app = Flask(__name__, template_folder='../templates/', static_folder='../static/', instance_relative_config=True)
    app.config.from_mapping({
        'TESTING' : False,
        'SQLALCHEMY_TRACK_MODIFICATIONS' : False,
        'SECRET_KEY' : 'dev',
    })

    
    if test_config is None:
        # load the instance of development config, when not testing
        try:
            from script.config import DevelopmentConfig
            app.config.from_object(DevelopmentConfig())
        except ModuleNotFoundError:
          pass
    else:
        # load the default test config and then load passed in test config
        try:
            from script.config import TestingConfig
            app.config.from_object(TestingConfig())
        except ModuleNotFoundError:
          pass
        app.config.from_mapping(test_config)
    
    from script.models import db
    db.init_app(app)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    

    return app