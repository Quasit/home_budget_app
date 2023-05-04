
from script.functions import get_allowed_budgets_list, get_used_by_list_by_expense_id, get_used_by_short, get_used_by_long

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

    assert expense1 == ['test_user']
    assert expense2 == ['second_test_user']
    assert expense4 == ['test_user', 'second_test_user']
    assert expense5 == ['test_user']
    assert expense6 == ['second_test_user']


def test_get_used_by_short(app_ctx):
    one_user = get_used_by_short(get_used_by_list_by_expense_id(1))
    two_users = get_used_by_short(get_used_by_list_by_expense_id(4))

    assert one_user == 'test_user'
    assert two_users == '2 osoby'


def test_get_used_by_long(app_ctx):
    one_user = get_used_by_long(get_used_by_list_by_expense_id(1))
    two_users = get_used_by_long(get_used_by_list_by_expense_id(4))

    assert one_user == 'test_user'
    assert two_users == 'test_user, second_test_user'
