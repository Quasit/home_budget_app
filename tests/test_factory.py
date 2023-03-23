from script import create_app


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_db(app):
    from script.models import User
    with app.app_context():
        user = User.query.filter_by(id=1).first()
        assert user.username == 'test_user'
