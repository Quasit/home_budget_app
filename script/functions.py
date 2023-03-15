from datetime import datetime, timedelta, date
from calendar import monthrange
from random import randint
from flask import g
from flask_login import current_user

from script.main import db, app
from script.models import User, Budget, Category, Expense, AllowedUsers, UsedBy


def sort_func(e):
  """ Function to sort data by date """
  return e['date']

def random_color():
    """ Function which returns random Hex color code """
    r = lambda: randint(0,255)
    return '#%02X%02X%02X' % (r(),r(),r())


def get_allowed_budgets_list(user_id):
    budgets = []
    allowed_budgets = AllowedUsers.query.filter_by(user_id=user_id).all()
    for budget in allowed_budgets:
        budgets.append(Budget.query.filter_by(id=budget.budget_id).first())
    return budgets


@app.before_request
def get_allowed_budgets():
    if 'allowed_budgets' not in g and current_user.is_authenticated:
        g.allowed_budgets = get_allowed_budgets_list(current_user.id)

    
@app.teardown_appcontext
def teardown_allowed_budgets(exception):
    g.pop('allowed_budgets', None)



def get_used_by_list_by_expense_id(expense_id):
    """ Function takes expense_id and returns list with usernames from UsedBy table which is related to expense_id """
    database_used_by_records = UsedBy.query.filter_by(expense_id=expense_id).all()
    used_by_list = [User.query.filter_by(id=record.user_id).first().username for record in database_used_by_records]
    return used_by_list


def get_used_by_short(used_by_list):
    """ Function takes list of usernames and if it's just 1 user return string with it's username,
        or if there is more users it return string with quantity.
        It needs some conditions for polish plural form of 'person' """
    used_by_short = ''
    if len(used_by_list) == 1:
        used_by_short = used_by_list[0]
    elif len(used_by_list) >= 2 and len(used_by_list) < 5:
        used_by_short = str(len(used_by_list)) + ' osoby'
    elif len(used_by_list) >= 5:
        used_by_short = str(len(used_by_list)) + ' osób'
    return used_by_short


def get_used_by_long(used_by_list):
    """ Function takes list of usernames and returns string of those usernames separated with comma """
    used_by_long = ''
    for name in used_by_list:
        used_by_long+= name + ', '
    used_by_long = used_by_long[:-2]
    return used_by_long


def get_categories_dict(budget_id):
    """ Function takes budget_id and returns dictionary of categories with it's name and description in schema:
        category_dict[category.id] = [category.name, category.description] """
    categories = Category.query.filter_by(budget_id=budget_id).all()
    category_dict = {}
    for category in categories:
        category_dict[category.id] = [category.name, category.description]
    return category_dict


def get_expenses(budget_id):
    """ Function takes budget_id and returns list of expenses(dictionaries).\n
        Each expense in list is dictionary with such keys
            "id": expense.id,
            "name": expense.name,
            "description": expense.description,
            "date": expense.date,
            "category_id": expense.category_id (Category table id),
            "category_name": category.name,
            "category_description": category.description,
            "amount": expense.amount (float number),
            "payer_id": expense.payer (User table id),
            "payer_name": user.username,
            "used_by": string with number of users (or if 1 user -> it's User.username),
            "used_by_full_description": string with all User.username separated by comma """
    
    category_dict = get_categories_dict(budget_id)
    expenses = Expense.query.filter_by(budget_id=budget_id).all()
    expenses_list = []
    for expense in expenses:
        used_by_list = get_used_by_list_by_expense_id(expense.id)
        used_by_short = get_used_by_short(used_by_list)
        used_by_full_description = get_used_by_long(used_by_list)

        expense_dict = {
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
            "used_by": used_by_short,
            "used_by_full_description": used_by_full_description
        }
        expenses_list.append(expense_dict)
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

    # This loop puts category names into categories_labels list,
    # color codes of those categories into categories_colors list,
    # and sums expenses by categories and puts sum data into dictionary
    # with pair: category name as key - and sum amount as value
    for expense, category in expense_list:
        if category.name not in categories_labels:
            categories_labels.append(category.name)
            categories_colors.append(category.color)
        try:
            categories_summary[category.name] += float(expense.amount)
        except:
            categories_summary[category.name] = float(expense.amount)

    # This loop preparing list of only category sum values (pure numbers) used later to generate chart
    for cat in categories_labels:
        categories_dataset.append(categories_summary[cat])

    # This loop set values in categories_summary dictionary to be 2 digits after . sign
    for cat, amount in categories_summary.items():
        categories_summary[cat] = '%.2f' % amount

    return {
        "total": '%.2f' % sum(categories_dataset),
        "categories_summary": categories_summary,
        "categories_labels": categories_labels,
        "categories_colors": categories_colors,
        "categories_dataset": categories_dataset
    }


def get_allowed_users(budget_id):
    """ Function takes budget_id and returns list of User.id's from AllowedUsers table"""
    allowed_users = AllowedUsers.query.filter_by(budget_id=budget_id).all()
    allowed_users_list = [user.id for user in allowed_users]
    return allowed_users_list
