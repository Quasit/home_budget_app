from script import create_app


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_db(app_ctx, db):
    assert repr(db.engine.url) == 'sqlite:///:memory:'