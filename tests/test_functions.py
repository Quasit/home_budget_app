import pytest
from datetime import datetime, timedelta
from calendar import monthrange
from script.functions import (get_allowed_budgets_list, get_used_by_list_by_expense_id,
                              get_used_by_short, get_used_by_long, get_categories_dict,
                              get_expenses, get_default_period_dates, get_expenses_from_period,
                              get_expense_summary, get_allowed_users_ids)

def test_get_allowed_budgets_list(app_ctx):
    budgets_user1 = get_allowed_budgets_list(1)
    budgets_user2 = get_allowed_budgets_list(2)
    
    assert len(budgets_user1) == 1
    assert len(budgets_user2) == 2

    budgets_user2_ids = []
    for budget in budgets_user2:
        budgets_user2_ids.append(budget.id)

    assert budgets_user1[0].id == 1
    assert budgets_user2_ids == [1, 2]


def test_get_used_by_list_by_expense_id(app_ctx):
    expense1 = get_used_by_list_by_expense_id(1)
    expense2 = get_used_by_list_by_expense_id(2)
    expense4 = get_used_by_list_by_expense_id(4)
    expense5 = get_used_by_list_by_expense_id(5)
    expense6 = get_used_by_list_by_expense_id(6)
    expense7 = get_used_by_list_by_expense_id(7)

    assert expense1 == ['test_user']
    assert expense2 == ['second_test_user']
    assert expense4 == ['test_user', 'second_test_user']
    assert expense5 == ['test_user']
    assert expense6 == ['second_test_user']
    assert expense7 == ['test_user', 'second_test_user', 'third_test_user',
                        'fourth_test_user', 'fifth_test_user']


def test_get_used_by_short(app_ctx):
    one_user = get_used_by_short(get_used_by_list_by_expense_id(1))
    two_users = get_used_by_short(get_used_by_list_by_expense_id(4))
    five_users = get_used_by_short(get_used_by_list_by_expense_id(7))

    assert one_user == 'test_user'
    assert two_users == '2 osoby'
    assert five_users == '5 osób'


def test_get_used_by_long(app_ctx):
    one_user = get_used_by_long(get_used_by_list_by_expense_id(1))
    two_users = get_used_by_long(get_used_by_list_by_expense_id(4))
    five_users = get_used_by_long(get_used_by_list_by_expense_id(7))

    assert one_user == 'test_user'
    assert two_users == 'test_user, second_test_user'
    assert five_users == 'test_user, second_test_user, third_test_user, fourth_test_user, fifth_test_user'


def test_get_categories_dict(app_ctx):
    categories = get_categories_dict(1)
    empty_cat = get_categories_dict(2)

    assert categories == {1: ['test_category1', 'test_category_1_description'],
                          2: ['test_category2', 'test_category_2_description']}
    assert empty_cat == {}


def test_get_expenses(app_ctx):
    expenses = get_expenses(1)
    
    expense_1 = {
        "id": 1,
        "name": 'test_expense1',
        "description": 'test_expense_1_description',
        "date": datetime.today().date(),
        "category_id": 1,
        "category_name": 'test_category1',
        "category_description": 'test_category_1_description',
        "amount": 100.01,
        "payer_id": 1,
        "payer_name": 'test_user',
        "used_by": 'test_user',
        "used_by_full_description": 'test_user'
    }
    
    expense_7 = {
        "id": 7,
        "name": 'test_expense7',
        "description": 'test_expense_7_description',
        "date": datetime.strptime('1999-01-01', '%Y-%m-%d').date(),
        "category_id": 2,
        "category_name": 'test_category2',
        "category_description": 'test_category_2_description',
        "amount": 200.00,
        "payer_id": 2,
        "payer_name": 'second_test_user',
        "used_by": '5 osób',
        "used_by_full_description": 'test_user, second_test_user, third_test_user, fourth_test_user, fifth_test_user'
    }

    assert len(expenses) == 7
    assert expenses[0] == expense_1
    assert expenses[-1] == expense_7

    empty_expenses = get_expenses(2)

    assert empty_expenses == []


def test_get_default_period_dates(app_ctx):
    
    with pytest.raises(Exception) as no_period_case:
        get_default_period_dates()
    assert str(no_period_case.value) == "Period not specified"

    with pytest.raises(Exception) as wrong_period_case:
        get_default_period_dates('wrong_period')
    assert str(wrong_period_case.value) == "Wrong period, should be one from the list: ['this_month', 'this_year', 'one_year']"

    today = datetime.today().date()

    this_month_begin = today.replace(day=1).date()
    this_month_end = today.replace(day=monthrange(today.year, today.month)[1]).date()
    this_month = get_default_period_dates('this_month')
    assert this_month == (this_month_begin, this_month_end)

    this_year_begin = today.replace(month=1, day=1).date()
    this_year_end = today.replace(month=12, day=31).date()
    this_year = get_default_period_dates('this_year')
    assert this_year == (this_year_begin, this_year_end)
    
    one_year_period_begin = (today - timedelta(weeks=52)).date()
    one_year = get_default_period_dates('one_year')
    assert one_year == (one_year_period_begin, today)


def test_get_expenses_from_period(app_ctx):
    with pytest.raises(Exception) as none_arguments_case:
        get_expenses_from_period()
    assert str(none_arguments_case.value) == "At least one passed argument is not specified"

    with pytest.raises(Exception) as one_argument_case:
        get_expenses_from_period(1)
    assert str(one_argument_case.value) == "At least one passed argument is not specified"

    with pytest.raises(Exception) as two_arguments_case:
        get_expenses_from_period(1, 2)
    assert str(two_arguments_case.value) == "At least one passed argument is not specified"

    with pytest.raises(TypeError) as wrong_date_format:
        get_expenses_from_period(1, str(datetime.today()), datetime.today().date())
    assert str(wrong_date_format.value) == "Wrong date type, dates should be in datetime.date type"

    with pytest.raises(TypeError) as wrong_second_date_format:
        get_expenses_from_period(1, datetime.today(), datetime.today().time())
    assert str(wrong_second_date_format.value) == "Wrong date type, dates should be in datetime.date type"




    today_expenses = get_expenses_from_period(1, datetime.today().date(), datetime.today().date())

    assert len(today_expenses) == 1
    assert today_expenses[0][0].name == 'test_expense1'
    assert today_expenses[0][1].name == 'test_category1'

    # Three expenses have date : 2021-06-15

    date = datetime.strptime('2021-06-15', '%Y-%m-%d').date()

    expenses = get_expenses_from_period(1, date, date)

    assert len(expenses) == 3

    # One expense have date : 2022-06-30
    date2 = datetime.strptime('2022-06-30', '%Y-%m-%d').date()
    expenses2 = get_expenses_from_period(1, date, date2)

    assert len(expenses2) == 4

    with pytest.raises(Exception) as begin_date_bigger_case:
        get_expenses_from_period(1, date2, date)
    assert str(begin_date_bigger_case.value) == "begin_date cannot be higher than the end_date"


def test_get_expense_summary(app_ctx):
    # one test left to fill here
    pass


def test_get_allowed_users_ids(app_ctx):
    first_budget = get_allowed_users_ids(1)
    second_budget = get_allowed_users_ids(2)

    assert first_budget == [1, 2, 3, 4, 5]
    assert second_budget == [2]
