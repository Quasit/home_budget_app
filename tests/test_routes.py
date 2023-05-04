from flask_login import current_user

def test_index_not_logged_in(client):
    response = client.get('/')
    assert b"Zaloguj" in response.data
    assert b"Zarejestruj" in response.data


def test_index_logged_in(client_logged_usr1):
    response = client_logged_usr1.get('/')
    assert b"Wyloguj" in response.data


def test_get_allowed_budgets_usr1(client_logged_usr1):
    # User 1 should see only test_budget_1
    # test_budget_2 should NOT be visible for user 1
    response = client_logged_usr1.get('/')
    assert b"test_budget_1" in response.data
    assert b"test_budget_2" not in response.data


def test_allowed_budgets_usr2(client_logged_usr2):
    # User 2 should see test_budget_1 and test_budget_2
    response = client_logged_usr2.get('/')
    assert b"test_budget_1" in response.data
    assert b"test_budget_2" in response.data


def test_my_budgets_route(client_logged_usr2):
    response = client_logged_usr2.get('/my_budgets')
    assert b"test_budget_1_description" in response.data
    assert b"test_budget_2_description" in response.data
