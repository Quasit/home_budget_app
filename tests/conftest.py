import pytest
from script import create_app
from tests.add_test_data import add_test_data
from script.routes import general
from script.models import create_tables_if_not_exist, User
from flask_login import FlaskLoginClient

def pytest_configure(config):
    config.addinivalue_line("markers", "index: index route tests")
    config.addinivalue_line("markers", "register: register route tests")
    config.addinivalue_line("markers", "login: login route tests")
    config.addinivalue_line("markers", "logout: logout route tests")
    config.addinivalue_line("markers", "my_budgets: my_budgets route tests")
    config.addinivalue_line("markers", "add_budget: add_budget route tests")
    config.addinivalue_line("markers", "budget_summary: /budget/<int:budget_id> route tests")


@pytest.fixture
def app():
    
    app = create_app({
        'TESTING': True,
        'WTF_CSRF_ENABLED' : False
    })

    with app.app_context():
        create_tables_if_not_exist(app)
        add_test_data()

    app.register_blueprint(general)
    
    app.test_client_class = FlaskLoginClient
    
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def app_ctx(app):
    with app.app_context():
        yield


@pytest.fixture
def client_logged_usr1(app, app_ctx):
    user = User.query.get(1)
    return app.test_client(user=user)


@pytest.fixture
def client_logged_usr2(app, app_ctx):
    user = User.query.get(2)
    return app.test_client(user=user)


@pytest.fixture
def db():
    from script.models import db
    return db