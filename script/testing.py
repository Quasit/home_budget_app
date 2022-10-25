from main import db
from models import Category

category = Category.query.filter_by(budget_id=1, name='Jedzenie').first()

print(category.id)