from flask import Flask
import os
import time

    

def create_app(test_config=None):
    app = Flask(__name__, template_folder='../templates/', static_folder='../static/', instance_relative_config=True)
    app.config.from_mapping({
        'TESTING' : False,
        'SQLALCHEMY_DATABASE_URI' : 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS' : False,
        
    })
    
    if test_config is None:
        # if run on docker load environment config variables
        if os.environ.get('ENVIRONMENT') == 'docker' or os.environ.get('ENVIRONMENT') == 'kubernetes':
            app.config.from_prefixed_env()
            # check if all data needed to set up postgres connection is not empty
            if os.environ.get('POSTGRES_USER') and os.environ.get('POSTGRES_PASSWORD') and os.environ.get('POSTGRES_HOST'):
                app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{}:{}@{}:{}/home_budget'.format(
                    os.environ.get('POSTGRES_USER'),
                    os.environ.get('POSTGRES_PASSWORD'),
                    os.environ.get('POSTGRES_HOST'),
                    os.environ.get('POSTGRES_PORT'))
            else:
                raise RuntimeError("The environment variables for  is not set")
            
        else:  # if no environment variables then load local config.py file
            try:
                from script.config import DevelopmentConfig
                app.config.from_object(DevelopmentConfig())       
            except ModuleNotFoundError:
                pass
    else:
        # load test config
        app.config.from_mapping(test_config)
    
    from script.models import db, create_tables_if_not_exist
    connected = False
    tries = 0
    while not connected and tries < 10:
        try:
            print("Trying to connect to database")
            db.init_app(app)
            connected = True
        except:
            print("Connection failed next try in 2 seconds")
            time.sleep(2)
            tries += 1
    if not connected:
        raise RuntimeError("Cannot connect to database")
    create_tables_if_not_exist(app)

    from script.routes import login_manager
    login_manager.init_app(app)

    return app