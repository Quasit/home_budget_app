from datetime import datetime, timedelta, date
from calendar import monthrange
from random import randint

from main import db
from models import User, Budget, Category, Expense


def sort_func(e):
  return e['date']

def random_color():
    r = lambda: randint(0,255)
    return '#%02X%02X%02X' % (r(),r(),r())
    

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
        expenses_list.sort(key=sort_func, reverse=True)
    return expenses_list


def get_default_period_dates(period=None):
    """ Takes 1 argument "period" ["this_month"/"this_year"/"one_year"] and returns "begin_date" and "end_date\n
        If passed argument is different, or there is no argument raises Exception Error """
    if period == None:
        raise Exception("Period not specified")

    today = datetime.today()

    if period == "this_month":
        this_month_begin = today.replace(day=1).date()
        this_month_end = today.replace(day=monthrange(this_month_begin.year, this_month_begin.month)[1]).date()
        return this_month_begin, this_month_end

    elif period == "this_year":
        this_year_begin = today.replace(month=1, day=1).date()
        this_year_end = today.replace(month=12, day=31).date()
        return this_year_begin, this_year_end

    elif period == "one_year":
        one_year_period_begin = (today - timedelta(weeks=52)).date()
        return one_year_period_begin, today
    
    raise Exception("Wrong period, should be one from the list: ['this_month', 'this_year', 'one_year']")

def get_expenses_from_period(budget_id= None, begin_date=None, end_date=None):
    """ Takes 3 arguments "budget_id", "begin_date" and "end_date" and returns list of all expenses between those dates
        If at least 1 argument is not specified raises Exception Error"""
    if budget_id is None or begin_date is None or end_date is None:
        raise Exception("At least one passed argument is not specified")
    if not isinstance(begin_date, date) or not isinstance(end_date, date):
        raise TypeError('Wrong date type, dates should be in datetime.date type')
    expenses = db.session.query(Expense, Category).filter_by(budget_id=budget_id).filter(Expense.date >= begin_date, Expense.date <= end_date).order_by(Expense.date).join(Category).all()
    return expenses

def get_expense_summary(expense_list):
    """ Takes expense and category list from "get_expense_from_period" function and returns dictionary with fields:\n
        "total": sum of all expenses in list\n
        "categories_summary": dictionary of category names as keys, and sum of expenses in that category as values\n
        "categories_labels": list of category names (for chart)\n
        "categories_colors": list of HEX colors set for categories (for chart)\n
        "categories_dataset": list of categories expenses summed amounts (for chart)
    """
    categories_labels = []
    categories_colors = []
    categories_dataset = []
    categories_summary = {}

    for expense, category in expense_list:
        if category.name not in categories_labels:
            categories_labels.append(category.name)
            categories_colors.append(category.color)
        try:
            categories_summary[category.name] += float(expense.amount)
        except:
            categories_summary[category.name] = float(expense.amount)

    for cat in categories_labels:
        categories_dataset.append(categories_summary[cat])

    for cat, amount in categories_summary.items():
        categories_summary[cat] = '%.2f' % amount

    return {
        "total": '%.2f' % sum(categories_dataset),
        "categories_summary": categories_summary,
        "categories_labels": categories_labels,
        "categories_colors": categories_colors,
        "categories_dataset": categories_dataset
    }
