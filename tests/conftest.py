import pytest
from script import create_app
from script.create_tables import create_tables
from tests.add_test_data import add_test_data


@pytest.fixture
def app():
    
    app = create_app({
        'TESTING': True,
    })

    with app.app_context():
        create_tables()
        add_test_data()
    
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
