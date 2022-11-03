from main import db
from models import User, Budget, Category, Expense

def sort_func(e):
  return e['date']

def get_expenses(budget_id):
    categories = Category.query.filter_by(budget_id=budget_id).all()
    category_dict = {}
    for category in categories:
        category_dict[category.id] = [category.name, category.description]
    
    expenses = Expense.query.filter_by(budget_id=budget_id).all()
    expenses_list = []
    for expense in expenses:
        expense_json = {
            "id": expense.id,
            "name": expense.name,
            "description": expense.description,
            "date": expense.date,
            "category_id": expense.category_id,
            "category_name": category_dict[expense.category_id][0],
            "category_description": category_dict[expense.category_id][1],
            "amount": float(expense.amount),
            "payer_id": expense.payer,
            "payer_name": User.query.get(expense.payer).username,
            "used_by": expense.used_by.username
        }
        expenses_list.append(expense_json)
        expenses_list.sort(key=sort_func)
    return expenses_list