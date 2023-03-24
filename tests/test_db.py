from sqlalchemy import inspect


def test_db_tables(app_ctx, db):
    inspector = inspect(db.engine)
    assert inspector.has_table("user")
    assert inspector.has_table("budget")
    assert inspector.has_table("allowed_users")
    assert inspector.has_table("category")
    assert inspector.has_table("expense")
    assert inspector.has_table("used_by")