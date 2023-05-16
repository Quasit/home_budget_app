from script.models import User, Budget, AllowedUsers
import pytest

def response_to_file(response):
    with open("tests/response_data.txt", "w") as response_file:
        response_file.write(response.data.decode())


# CURRENT ROUTES
# '/' - DONE
# '/register' - DONE
# '/login' - DONE
# '/logout' - DONE
# '/my_budgets' - DONE
# '/budget/add_budget' - DONE
# '/budget/<int:budget_id>'
# '/budget/<int:budget_id>/expenses'
# '/budget/<int:budget_id>/add_expense'
# '/budget/<int:budget_id>/edit_expense/<int:expense_id>'
# '/budget/<int:budget_id>/remove_expense/<int:expense_id>'
# '/budget/<int:budget_id>/add_category'
# '/budget/<int:budget_id>/edit_category/<int:category_id>'
# '/budget/<int:budget_id>/remove_category/<int:category_id>'
# '/budget/<int:budget_id>/settings'

# ----------------------------
# '/' index TESTS
# ----------------------------

@pytest.mark.index
def test_base_index(client):
    response = client.get('/')
    assert "Strona główna".encode() in response.data


@pytest.mark.index
def test_index_not_logged_in(client):
    response = client.get('/')
    assert b"Zaloguj" in response.data
    assert b"Zarejestruj" in response.data


@pytest.mark.index
def test_index_logged_in(client_logged_usr1):
    response = client_logged_usr1.get('/')
    assert b"Wyloguj" in response.data


@pytest.mark.index
def test_get_allowed_budgets_usr1(client_logged_usr1):
    # User 1 should see only test_budget_1
    # test_budget_2 should NOT be visible for user 1
    response_usr1 = client_logged_usr1.get('/')
    assert b"test_budget_1" in response_usr1.data
    assert b"test_budget_2" not in response_usr1.data


@pytest.mark.index
def test_get_allowed_budgets_usr2(client_logged_usr2):
    # User 2 should see test_budget_1 and test_budget_2
    response_usr2 = client_logged_usr2.get('/')
    assert b"test_budget_1" in response_usr2.data
    assert b"test_budget_2" in response_usr2.data


# ----------------------------
# '/register' TESTS
# ----------------------------

@pytest.mark.register
def test_register_get(client):
    response = client.get('/register')
    assert '<label for="username">Nazwa użytkownika</label>'.encode() in response.data
    assert '<input id="username" name="username" required size="32" type="text" value="">'.encode() in response.data
    assert '<label for="email">E-mail</label>'.encode() in response.data
    assert '<input id="email" name="email" required size="32" type="text" value="">'.encode() in response.data
    assert '<label for="password">Hasło</label>'.encode() in response.data
    assert '<input id="password" name="password" required size="32" type="password" value="">'.encode() in response.data
    assert '<label for="password2">Powtórz Hasło</label>'.encode() in response.data
    assert '<input id="password2" name="password2" required size="32" type="password" value="">'.encode() in response.data
    assert '<input id="submit" name="submit" type="submit" value="Zarejestruj">'.encode() in response.data


@pytest.mark.register
def test_register_post(client, app_ctx):
    form_data = {'username': 'test_post_username',
        'email': 'test_post@email.com',
        'password': 'testpostpassword',
        'password2': 'testpostpassword'
        }
    response = client.post('/register', data=form_data)
    assert response.status_code == 302

    user = User.query.filter_by(username='test_post_username').first()
    assert user.username == 'test_post_username'


@pytest.mark.register
def test_register_post_taken_data(client):
    form_data = {'username': 'test_user',
        'email': 'test2@email.com',
        'password': 'testpostpassword',
        'password2': 'testpostpassword'
        }
    response = client.post('/register', data=form_data)
    assert response.status_code == 200
    assert 'Ta nazwa użytkownika jest już zajęta. Proszę użyć innej nazwy użytkownika.'.encode() in response.data
    assert 'Ten adres email jest już zajęty. Proszę użyć innego adresu email.'.encode() in response.data


@pytest.mark.register
def test_register_post_wrong_data(client):
    form_data = {'username': 'test_post_username',
        'email': 'email',
        'password': 'testpostpassword',
        'password2': 'wrong_password'
        }
    response = client.post('/register', data=form_data)
    assert response.status_code == 200
    assert 'Nieprawidłowy format adresu email'.encode() in response.data
    assert 'Hasła nie mogą się różnić'.encode() in response.data


@pytest.mark.register
def test_register_post_empty_data(client):
    username_err = 'Pole Nazwa użytkownika nie może być puste.'
    email_err = 'Pole E-mail nie może być puste.'
    password_err = 'Pole Hasło nie może być puste.'
    password2_err = 'Pole Powtórz Hasło nie może być puste.'
    form_data = {'username': '',
        'email': '',
        'password': '',
        'password2': ''
        }
    response = client.post('/register', data=form_data)
    assert response.status_code == 200
    assert username_err.encode() in response.data
    assert email_err.encode() in response.data
    assert password_err.encode() in response.data
    assert password2_err.encode() in response.data


# ----------------------------
# '/login' TESTS
# ----------------------------

@pytest.mark.login
def test_login_get(client):
    response = client.get('/login')
    assert '<label for="username">Nazwa użytkownika</label>'.encode() in response.data
    assert '<input id="username" name="username" required size="32" type="text" value="">'.encode() in response.data
    assert '<label for="password">Hasło</label>'.encode() in response.data
    assert '<input id="password" name="password" required size="32" type="password" value="">'.encode() in response.data
    assert '<label for="remember_me">Zapamiętaj mnie</label>'.encode() in response.data
    assert '<input id="remember_me" name="remember_me" type="checkbox" value="y">'.encode() in response.data
    assert '<input id="submit" name="submit" type="submit" value="Zaloguj">'.encode() in response.data


@pytest.mark.login
def test_login_post(client):
    form_data = {'username': 'test_post_username',
                 'password': 'testpostpassword',
                 'remember_me' : False
                 }
    response = client.post('/login', data=form_data)
    assert response.status_code == 302


@pytest.mark.login
def test_login_post_redirect(client):
    form_data = {'username': 'test_user',
                 'password': 'test',
                 'remember_me': False
                 }
    response = client.post('/login', data=form_data, follow_redirects=True)
    assert response.status_code == 200
    assert b"Wyloguj" in response.data


@pytest.mark.login
def test_login_post_wrong_username(client):
    form_data = {'username': 'wrong_username',
                 'password': 'test',
                 'remember_me': False
                 }
    response = client.post('/login', data=form_data, follow_redirects=True)
    assert response.status_code == 200
    assert 'Invalid username or password'.encode() in response.data


@pytest.mark.login
def test_login_post_wrong_password(client):
    form_data = {'username': 'test_user',
                 'password': 'wrong_password',
                 'remember_me': False
                 }
    response = client.post('/login', data=form_data, follow_redirects=True)
    assert response.status_code == 200
    assert 'Invalid username or password'.encode() in response.data


@pytest.mark.login
def test_login_post_empty_data(client):
    username_err = 'Pole Nazwa użytkownika nie może być puste.'
    password_err = 'Pole Hasło nie może być puste.'
    form_data = {'username': '',
        'password': '',
        'remember_me': False
        }
    response = client.post('/login', data=form_data)
    assert response.status_code == 200
    assert username_err.encode() in response.data
    assert password_err.encode() in response.data


# ----------------------------
# '/logout' TESTS
# ----------------------------

@pytest.mark.logout
def test_logout(client_logged_usr1):
    response = client_logged_usr1.get('/')
    assert b"Wyloguj" in response.data
    response = client_logged_usr1.get('/logout', follow_redirects=True)
    assert b"Zaloguj" in response.data


# ----------------------------
# '/my_budgets' TESTS
# ----------------------------

@pytest.mark.my_budgets
def test_my_budgets_route(client_logged_usr1):
    response_usr1 = client_logged_usr1.get('/my_budgets')
    assert b"test_budget_1</a> - test_budget_1_description</h3>" in response_usr1.data
    assert b"test_budget_2</a> - test_budget_2_description</h3>" not in response_usr1.data


@pytest.mark.my_budgets
def test_my_budgets_route(client_logged_usr2):
    response_usr2 = client_logged_usr2.get('/my_budgets')
    assert b"test_budget_1</a> - test_budget_1_description</h3>" in response_usr2.data
    assert b"test_budget_2</a> - test_budget_2_description</h3>" in response_usr2.data


# ----------------------------
# '/budget/add_budget' TESTS
# ----------------------------

@pytest.mark.add_budget
def test_add_budget_get(client_logged_usr1):
    response = client_logged_usr1.get('/budget/add_budget')
    assert '<label for="name">Nazwa budżetu</label>'.encode() in response.data
    assert '<input id="name" name="name" required type="text" value="">'.encode() in response.data
    assert '<label for="description">Opis (opcjonalne)</label>'.encode() in response.data
    assert '<textarea id="description" name="description"></textarea>'.encode() in response.data
    assert '<input id="submit" name="submit" type="submit" value="Wyślij">'.encode() in response.data


@pytest.mark.add_budget
def test_add_budget_post(client_logged_usr1, app_ctx):
    form_data = {'name': 'test_post_budget',
                 'description': 'test post budget description',
                 }
    response = client_logged_usr1.post('/budget/add_budget', data=form_data)
    assert response.status_code == 302

    new_budget = Budget.query.filter_by(name='test_post_budget').first()
    assert new_budget.name == 'test_post_budget'
    assert new_budget.description == 'test post budget description'
    assert new_budget.owner_id == 1

    allowed_new_budget = AllowedUsers.query.filter_by(budget_id=new_budget.id).all()
    assert len(allowed_new_budget) == 1
    assert allowed_new_budget[0].user_id == 1
    assert allowed_new_budget[0].editor == True


@pytest.mark.add_budget
def test_add_budget_post_empty_name(client_logged_usr1, app_ctx):
    form_data = {'name': '',
                 'description': '',
                 }
    response = client_logged_usr1.post('/budget/add_budget', data=form_data)
    name_err = 'Pole Nazwa budżetu nie może być puste.'
    assert response.status_code == 200
    assert name_err.encode() in response.data


# ----------------------------
# '/budget/<int:budget_id>' TESTS
# ----------------------------

@pytest.mark.budget_summary
def test_budget_get_budget_menu(client_logged_usr1):
    response = client_logged_usr1.get('/budget/1')

    assert '<div class="budget-menu-form"><a class="budget-menu-a" href="/budget/1/settings">&#128736 Ustawienia</a></div>'.encode() in response.data
    assert '<div class="budget-menu-form"><a class="budget-menu-a" href="/budget/1/expenses">&#128197 Wydatki</a></div>'.encode() in response.data
    assert '<div class="budget-menu-form"><a class="budget-menu-a" href="/budget/1">&#128202 Podsumowanie</a></div>'.encode() in response.data


@pytest.mark.budget_summary
def test_budget_get_this_month_summary(client_logged_usr1):
    response = client_logged_usr1.get('/budget/1')
    assert '<td id="this_month-balance-expenses_total">100.01 zł</td>'.encode() in response.data
    assert '<td id="this_month-expenses-expenses_total">100.01 zł</td>'.encode() in response.data
    assert '<td id="this_month-expenses-category_name">test_category1</td>'.encode() in response.data
    assert '<td id="this_month-expenses-category_total">100.01 zł</td>'.encode() in response.data


@pytest.mark.budget_summary
def test_budget_get_this_year_summary(client_logged_usr1):
    response = client_logged_usr1.get('/budget/1')
    assert '<td id="this_year-balance-expenses_total">100.01 zł</td>'.encode() in response.data
    assert '<td id="this_year-expenses-expenses_total">100.01 zł</td>'.encode() in response.data
    assert '<td id="this_year-expenses-category_name">test_category1</td>'.encode() in response.data
    assert '<td id="this_year-expenses-category_total">100.01 zł</td>'.encode() in response.data


@pytest.mark.budget_summary
def test_budget_get_one_year_period_summary(client_logged_usr1):
    response = client_logged_usr1.get('/budget/1')
    assert '<td id="one_year_period-balance-expenses_total">180.01 zł</td>'.encode() in response.data
    assert '<td id="one_year_period-expenses-expenses_total">180.01 zł</td>'.encode() in response.data
    assert '<td id="one_year_period-expenses-category_name">test_category2</td>'.encode() in response.data
    assert '<td id="one_year_period-expenses-category_total">30.00 zł</td>'.encode() in response.data
    assert '<td id="one_year_period-expenses-category_name">test_category1</td>'.encode() in response.data
    assert '<td id="one_year_period-expenses-category_total">150.01 zł</td>'.encode() in response.data


@pytest.mark.budget_summary
def test_budget_get_chart_script(client_logged_usr1):
    response = client_logged_usr1.get('/budget/1')
    assert 'buildChart("chart_current_month", [\'test_category1\'], [100.01], [\'#ffffff\'])'.encode() in response.data
    assert 'buildChart("chart_current_year", [\'test_category1\'], [100.01], [\'#ffffff\'])'.encode() in response.data
    assert 'buildChart("chart_one_year_period", [\'test_category2\', \'test_category1\'], [30.0, 150.01], [\'#000000\', \'#ffffff\'])'.encode() in response.data
    
    
