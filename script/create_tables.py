def create_tables():
    from script.models import db, User, Budget, AllowedUsers, Category, Expense, UsedBy
    db.create_all()