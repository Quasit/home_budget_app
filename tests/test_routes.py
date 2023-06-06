from script.models import User, Budget, AllowedUsers, Expense, UsedBy, Category
from script.functions import get_expenses
import pytest
from datetime import datetime, timedelta
import re

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
# '/budget/<int:budget_id>' - DONE
# '/budget/<int:budget_id>/expenses' - DONE
# '/budget/<int:budget_id>/add_expense' - DONE
# '/budget/<int:budget_id>/edit_expense/<int:expense_id>' - DONE
# '/budget/<int:budget_id>/remove_expense/<int:expense_id>' - DONE
# '/budget/<int:budget_id>/settings' - DONE
# '/budget/<int:budget_id>/add_category' - DONE
# '/budget/<int:budget_id>/edit_category/<int:category_id>' - DONE
# '/budget/<int:budget_id>/remove_category/<int:category_id>' - DONE

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
def test_budget_summary_get_budget_menu(client_logged_usr1):
    response = client_logged_usr1.get('/budget/1')
    assert '<div class="budget-menu-form"><a class="budget-menu-a" href="/budget/1/settings">&#128736 Ustawienia</a></div>'.encode() in response.data
    assert '<div class="budget-menu-form"><a class="budget-menu-a" href="/budget/1/expenses">&#128197 Wydatki</a></div>'.encode() in response.data
    assert '<div class="budget-menu-form"><a class="budget-menu-a" href="/budget/1">&#128202 Podsumowanie</a></div>'.encode() in response.data


@pytest.mark.budget_summary
def test_budget_summary_get_this_month_summary(client_logged_usr1):
    response = client_logged_usr1.get('/budget/1')
    assert '<td id="this_month-balance-expenses_total">100.01 zł</td>'.encode() in response.data
    assert '<td id="this_month-expenses-expenses_total">100.01 zł</td>'.encode() in response.data
    assert '<td id="this_month-expenses-category_name">test_category1</td>'.encode() in response.data
    assert '<td id="this_month-expenses-category_total">100.01 zł</td>'.encode() in response.data


@pytest.mark.budget_summary
def test_budget_summary_get_this_year_summary(client_logged_usr1):
    response = client_logged_usr1.get('/budget/1')
    assert '<td id="this_year-balance-expenses_total">100.01 zł</td>'.encode() in response.data
    assert '<td id="this_year-expenses-expenses_total">100.01 zł</td>'.encode() in response.data
    assert '<td id="this_year-expenses-category_name">test_category1</td>'.encode() in response.data
    assert '<td id="this_year-expenses-category_total">100.01 zł</td>'.encode() in response.data


@pytest.mark.budget_summary
def test_budget_summary_get_one_year_period_summary(client_logged_usr1):
    response = client_logged_usr1.get('/budget/1')
    assert '<td id="one_year_period-balance-expenses_total">180.01 zł</td>'.encode() in response.data
    assert '<td id="one_year_period-expenses-expenses_total">180.01 zł</td>'.encode() in response.data
    assert '<td id="one_year_period-expenses-category_name">test_category2</td>'.encode() in response.data
    assert '<td id="one_year_period-expenses-category_total">30.00 zł</td>'.encode() in response.data
    assert '<td id="one_year_period-expenses-category_name">test_category1</td>'.encode() in response.data
    assert '<td id="one_year_period-expenses-category_total">150.01 zł</td>'.encode() in response.data


@pytest.mark.budget_summary
def test_budget_summary_get_chart_script(client_logged_usr1):
    response = client_logged_usr1.get('/budget/1')
    assert 'buildChart("chart_current_month", [\'test_category1\'], [100.01], [\'#ffffff\'])'.encode() in response.data
    assert 'buildChart("chart_current_year", [\'test_category1\'], [100.01], [\'#ffffff\'])'.encode() in response.data
    assert 'buildChart("chart_one_year_period", [\'test_category2\', \'test_category1\'], [30.0, 150.01], [\'#000000\', \'#ffffff\'])'.encode() in response.data


# ----------------------------
# '/budget/<int:budget_id>/expenses' TESTS
# ----------------------------

@pytest.mark.budget_expenses
def test_budget_expenses_get_menu(client_logged_usr1):
    response = client_logged_usr1.get('/budget/1/expenses')
    assert '<div class="budget-menu-form"><a class="budget-menu-a" href="/budget/1/settings">&#128736 Ustawienia</a></div>'.encode() in response.data
    assert '<div class="budget-menu-form"><a class="budget-menu-a" href="/budget/1/expenses">&#128197 Wydatki</a></div>'.encode() in response.data
    assert '<div class="budget-menu-form"><a class="budget-menu-a" href="/budget/1">&#128202 Podsumowanie</a></div>'.encode() in response.data


@pytest.mark.budget_expenses
def test_budget_expenses_get_add_expense_button(client_logged_usr1):
    response = client_logged_usr1.get('/budget/1/expenses')
    assert '<div class="add_expense_form"><a class="add_expense_a" href="/budget/1/add_expense">Dodaj wpis</a></div>'.encode() in response.data


@pytest.mark.budget_expenses
def test_budget_expenses_get_expenses_table(client_logged_usr1):
    expenses = get_expenses(budget_id=1)
    expenses_html_tables = []
    for expense in expenses:
        expense_html = f"""<tr>
                    <td>{expense['id']}.</td>
                    <td>{expense['date']}</td>
                    <td style="text-align:right; padding-right: 40px;"><b>{'%.2f' % expense['amount']} zł</b></td>
                    <td title="{expense['description']}">{expense['name']}</td>
                    <td title="{expense['category_description']}">{expense['category_name']}</td>
                    <td>{expense['payer_name']}</td>
                    <td title="{expense['used_by_full_description']}">{expense['used_by']}</td>
                    <td style="padding-right: 10px;">
                        <form action="/budget/1/remove_expense/{expense['id']}" onsubmit="return confirm('Czy na pewno chcesz usunąć ten wpis?\\n{expense['name']}')"><button title="Usuń wpis" class="remove_expense_btn" type="submit"><b>X</b></button></form>
                        <form><button title="Edytuj wpis" class="remove_expense_btn" type="submit" formaction="/budget/1/edit_expense/{expense['id']}"><b>&#9998</b></button></form>
                    </td>
                </tr>"""
        expenses_html_tables.append(expense_html)

    response = client_logged_usr1.get('/budget/1/expenses')
    for expense in expenses_html_tables:
        print(expense)
        assert expense.encode() in response.data


# ----------------------------
# '/budget/<int:budget_id>/add_expense' TESTS
# ----------------------------

@pytest.mark.add_expense
def test_add_expense_get(client_logged_usr1):
    response = client_logged_usr1.get('/budget/1/add_expense')
    
    assert '<div class="go_back_form"><a class="go_back_a" href="/budget/1/expenses">< Wstecz</a></div>'.encode() in response.data

    assert '<td><label for="name">Nazwa</label></td>'.encode() in response.data
    assert '<td><input id="name" name="name" required type="text" value=""></td>'.encode() in response.data
    assert '<td><label for="description">Opis (opcjonalne)</label></td>'.encode() in response.data
    assert '<td><textarea id="description" name="description"></textarea></td>'.encode() in response.data
    assert '<td><label for="category">Kategoria</label></td>'.encode() in response.data
    assert '<td><select id="category" name="category" required><option value="test_category1">test_category1</option><option value="test_category2">test_category2</option></select></td>'.encode() in response.data
    assert '<td><label for="amount">Kwota</label></td>'.encode() in response.data
    assert '<td><input id="amount" name="amount" required step="0.01" type="text" value=""></td>'.encode() in response.data
    assert '<td><label for="date">Data</label></td>'.encode() in response.data
    assert '<td><input id="date" name="date" required type="text" value=""></td>'.encode() in response.data
    assert '<td><label for="payer">Płaci</label></td>'.encode() in response.data
    assert '<td><select id="payer" name="payer" required><option value="test_user">test_user</option><option value="second_test_user">second_test_user</option><option value="third_test_user">third_test_user</option><option value="fourth_test_user">fourth_test_user</option><option value="fifth_test_user">fifth_test_user</option></select></td>'.encode() in response.data
    assert '<td><label for="used_by">Używa</label></td>'.encode() in response.data
    assert '<td><table id="used_by"><tr><th><label for="used_by-0">test_user</label></th><td><input id="used_by-0" name="used_by" type="checkbox" value="test_user"></td></tr><tr><th><label for="used_by-1">second_test_user</label></th><td><input id="used_by-1" name="used_by" type="checkbox" value="second_test_user"></td></tr><tr><th><label for="used_by-2">third_test_user</label></th><td><input id="used_by-2" name="used_by" type="checkbox" value="third_test_user"></td></tr><tr><th><label for="used_by-3">fourth_test_user</label></th><td><input id="used_by-3" name="used_by" type="checkbox" value="fourth_test_user"></td></tr><tr><th><label for="used_by-4">fifth_test_user</label></th><td><input id="used_by-4" name="used_by" type="checkbox" value="fifth_test_user"></td></tr></table></td>'.encode() in response.data
    assert '<td colspan="2" style="text-align: center;"><input id="submit" name="submit" type="submit" value="Wyślij"></td>'.encode() in response.data


@pytest.mark.add_expense
def test_add_expense_post(client_logged_usr1, app_ctx):
    form_data = {'name': 'test_post_expense',
                 'description': 'test post expense description',
                 'category': 'test_category1',
                 'amount': 98.70,
                 'date': datetime.today().date(),
                 'payer': 'fourth_test_user',
                 'used_by': ['third_test_user', 'fourth_test_user', 'fifth_test_user']
                 }
    response = client_logged_usr1.post('/budget/1/add_expense', data=form_data)
    assert response.status_code == 302

    new_expense = Expense.query.filter_by(name='test_post_expense').first()
    assert new_expense.id == 8
    assert new_expense.name == 'test_post_expense'
    assert new_expense.description == 'test post expense description'
    assert new_expense.budget_id == 1
    assert new_expense.category_id == 1
    assert new_expense.date == datetime.today().date()
    assert new_expense.amount == '98.7'
    assert new_expense.payer == 4
    
    new_used_by_list = UsedBy.query.filter_by(expense_id=new_expense.id).all()
    assert len(new_used_by_list) == 3


@pytest.mark.add_expense
def test_add_expense_post_empty(client_logged_usr1):
    form_data = {'name': '',
                 'description': '',
                 'category': '',
                 'amount': '',
                 'date': '',
                 'payer': '',
                 'used_by': []
                 }
    response = client_logged_usr1.post('/budget/1/add_expense', data=form_data)
    assert response.status_code == 200

    assert 'Pole Nazwa nie może być puste.'.encode() in response.data
    assert 'Pole Kategoria nie może być puste.'.encode() in response.data
    assert 'Pole Kwota nie może być puste.'.encode() in response.data
    assert 'Pole Data nie może być puste.'.encode() in response.data
    assert 'Pole Płaci nie może być puste.'.encode() in response.data
    assert 'Przynajmniej jedna opcja musi być zaznaczona'.encode() in response.data


@pytest.mark.add_expense
def test_add_expense_post_wrong_data(client_logged_usr1):
    form_data = {'name': 'test_wrong_data_expense',
                 'description': '',
                 'category': 'nonexisting_category',
                 'amount': -100.37,
                 'date': 'asd',
                 'payer': 'nonexisting_user',
                 'used_by': ['nonexisting_user']
                 }
    response = client_logged_usr1.post('/budget/1/add_expense', data=form_data)
    assert response.status_code == 200
    assert '<td id="expense_category_error">Not a valid choice</td>'.encode() in response.data
    assert '<td id="expense_amount_error">Kwota nie może być mniejsza lub równa 0</td>'.encode() in response.data
    # If DateField type cannot convert input into datetime.date it sets its data field to None. That's why it shows empty field error
    assert 'Pole Data nie może być puste.'.encode() in response.data
    assert '<td id="expense_payer_error">Not a valid choice</td>'.encode() in response.data
    assert '<td id="expense_used_by_error">&#39;nonexisting_user&#39; is not a valid choice for this field</td>'.encode() in response.data


@pytest.mark.add_expense
def test_add_expense_post_future_date(client_logged_usr1):
    form_data = {'name': 'test_post_expense',
                 'description': '',
                 'category': 'test_category1',
                 'amount': 10,
                 'date': (datetime.today() + timedelta(days=1)).date(),
                 'payer': 'fifth_test_user',
                 'used_by': ['fifth_test_user']
                 }
    response = client_logged_usr1.post('/budget/1/add_expense', data=form_data)
    assert response.status_code == 200
    assert 'Nie można użyć przyszłej daty'.encode() in response.data


# ----------------------------
# '/budget/<int:budget_id>/edit_expense/<int:expense_id>' TESTS
# ----------------------------

@pytest.mark.edit_expense
def test_edit_expense_get(client_logged_usr1):
    response = client_logged_usr1.get('/budget/1/edit_expense/3')

    assert '<div class="go_back_form"><a class="go_back_a" href="/budget/1/expenses">< Wstecz</a></div>'.encode() in response.data
    
    assert '<td><label for="name">Nazwa</label></td>'.encode() in response.data
    assert '<td><input id="name" name="name" required type="text" value="test_expense3"></td>'.encode() in response.data
    assert '<td><label for="description">Opis (opcjonalne)</label></td>'.encode() in response.data
    assert '<td><textarea id="description" name="description">test_expense_3_description</textarea></td>'.encode() in response.data
    assert '<td><label for="category">Kategoria</label></td>'.encode() in response.data
    assert '<td><select id="category" name="category" required><option value="test_category1">test_category1</option><option selected value="test_category2">test_category2</option></select></td>'.encode() in response.data
    assert '<td><label for="amount">Kwota</label></td>'.encode() in response.data
    assert '<td><input id="amount" name="amount" required step="0.01" type="text" value="30.00"></td>'.encode() in response.data
    assert '<td><label for="date">Data</label></td>'.encode() in response.data
    assert '<td><input id="date" name="date" required type="text" value="2022-06-30"></td>'.encode() in response.data
    assert '<td><label for="payer">Płaci</label></td>'.encode() in response.data
    assert '<td><select id="payer" name="payer" required><option selected value="test_user">test_user</option><option value="second_test_user">second_test_user</option><option value="third_test_user">third_test_user</option><option value="fourth_test_user">fourth_test_user</option><option value="fifth_test_user">fifth_test_user</option></select></td>'.encode() in response.data
    assert '<td><label for="used_by">Używa</label></td>'.encode() in response.data
    assert '<td><table id="used_by"><tr><th><label for="used_by-0">test_user</label></th><td><input checked id="used_by-0" name="used_by" type="checkbox" value="test_user"></td></tr><tr><th><label for="used_by-1">second_test_user</label></th><td><input id="used_by-1" name="used_by" type="checkbox" value="second_test_user"></td></tr><tr><th><label for="used_by-2">third_test_user</label></th><td><input id="used_by-2" name="used_by" type="checkbox" value="third_test_user"></td></tr><tr><th><label for="used_by-3">fourth_test_user</label></th><td><input id="used_by-3" name="used_by" type="checkbox" value="fourth_test_user"></td></tr><tr><th><label for="used_by-4">fifth_test_user</label></th><td><input id="used_by-4" name="used_by" type="checkbox" value="fifth_test_user"></td></tr></table></td>'.encode() in response.data
    assert '<td colspan="2" style="text-align: center;"><input id="submit" name="submit" type="submit" value="Zapisz"></td>'.encode() in response.data


@pytest.mark.edit_expense
def test_edit_expense_post(client_logged_usr1, app_ctx):
    form_data = {'name': 'test_post_edit_expense_3',
                 'description': 'test post edit expense 3 description',
                 'category': 'test_category2',
                 'amount': 35.00,
                 'date': datetime.today().date(),
                 'payer': 'third_test_user',
                 'used_by': ['third_test_user', 'fifth_test_user']
                 }
    response = client_logged_usr1.post('/budget/1/edit_expense/3', data=form_data)
    assert response.status_code == 302

    edited_expense = Expense.query.filter_by(name='test_post_edit_expense_3').first()
    assert edited_expense.id == 3
    assert edited_expense.name == 'test_post_edit_expense_3'
    assert edited_expense.description == 'test post edit expense 3 description'
    assert edited_expense.budget_id == 1
    assert edited_expense.category_id == 2
    assert edited_expense.date == datetime.today().date()
    assert edited_expense.amount == '35.0'
    assert edited_expense.payer == 3

    new_used_by_list = UsedBy.query.filter_by(expense_id=edited_expense.id).all()
    assert len(new_used_by_list) == 2
    assert new_used_by_list[0].user_id == 3
    assert new_used_by_list[1].user_id == 5
    

@pytest.mark.edit_expense
def test_edit_expense_post_empty(client_logged_usr1):
    form_data = {'name': '',
                 'description': '',
                 'category': '',
                 'amount': '',
                 'date': '',
                 'payer': '',
                 'used_by': []
                 }
    response = client_logged_usr1.post('/budget/1/edit_expense/3', data=form_data)
    assert response.status_code == 200

    assert 'Pole Nazwa nie może być puste.'.encode() in response.data
    assert 'Pole Kategoria nie może być puste.'.encode() in response.data
    assert 'Pole Kwota nie może być puste.'.encode() in response.data
    assert 'Pole Data nie może być puste.'.encode() in response.data
    assert 'Pole Płaci nie może być puste.'.encode() in response.data
    assert 'Przynajmniej jedna opcja musi być zaznaczona'.encode() in response.data


@pytest.mark.edit_expense
def test_edit_expense_post_wrong_data(client_logged_usr1):
    form_data = {'name': 'test_wrong_data_expense',
                 'description': '',
                 'category': 'nonexisting_category',
                 'amount': -100.37,
                 'date': 'asd',
                 'payer': 'nonexisting_user',
                 'used_by': ['nonexisting_user']
                 }
    response = client_logged_usr1.post('/budget/1/edit_expense/3', data=form_data)
    assert response.status_code == 200

    assert '<td id="expense_category_error">Not a valid choice</td>'.encode() in response.data
    assert '<td id="expense_amount_error">Kwota nie może być mniejsza lub równa 0</td>'.encode() in response.data
    # If DateField type cannot convert input into datetime.date it sets its data field to None. That's why it shows empty field error
    assert 'Pole Data nie może być puste.'.encode() in response.data
    assert '<td id="expense_payer_error">Not a valid choice</td>'.encode() in response.data
    assert '<td id="expense_used_by_error">&#39;nonexisting_user&#39; is not a valid choice for this field</td>'.encode() in response.data


@pytest.mark.edit_expense
def test_edit_expense_post_future_date(client_logged_usr1):
    form_data = {'name': 'test_post_expense',
                 'description': '',
                 'category': 'test_category1',
                 'amount': 10,
                 'date': (datetime.today() + timedelta(days=1)).date(),
                 'payer': 'fifth_test_user',
                 'used_by': ['fifth_test_user']
                 }
    response = client_logged_usr1.post('/budget/1/edit_expense/3', data=form_data)
    assert response.status_code == 200

    assert 'Nie można użyć przyszłej daty'.encode() in response.data


# ----------------------------
# '/budget/<int:budget_id>/remove_expense/<int:expense_id>' TESTS
# ----------------------------

@pytest.mark.remove_expense
def test_remove_expense_get(client_logged_usr1, app_ctx):
    expense = Expense.query.get(6)
    assert expense is not None

    response = client_logged_usr1.get('/budget/1/remove_expense/6')
    assert response.status_code == 302

    expense = Expense.query.get(6)
    assert expense is None

    response = client_logged_usr1.get('/budget/1/remove_expense/6')
    assert response.status_code == 302

    response = client_logged_usr1.get('/budget/1/remove_expense/6', follow_redirects = True)
    assert response.status_code == 200
    assert response.request.path == "/budget/1/expenses"


# ----------------------------
# '/budget/<int:budget_id>/settings' TESTS
# ----------------------------

@pytest.mark.budget_settings
def test_budget_setting_get_budget_menu(client_logged_usr1):
    response = client_logged_usr1.get('/budget/1/settings')
    assert '<div class="budget-menu-form"><a class="budget-menu-a" href="/budget/1/settings">&#128736 Ustawienia</a></div>'.encode() in response.data
    assert '<div class="budget-menu-form"><a class="budget-menu-a" href="/budget/1/expenses">&#128197 Wydatki</a></div>'.encode() in response.data
    assert '<div class="budget-menu-form"><a class="budget-menu-a" href="/budget/1">&#128202 Podsumowanie</a></div>'.encode() in response.data


@pytest.mark.budget_settings
def test_budget_settings_get(client_logged_usr1):
    response = client_logged_usr1.get('/budget/1/settings')
    assert response.status_code == 200

    assert '<a class="add_expense_a" href="/budget/1/add_category">Dodaj kategorię</a>'.encode() in response.data

    assert '<td id="settings_category_color"><div style="background: #ffffff; min-height:20px; min-width:20px; margin:2px"></div></td>'.encode() in response.data
    assert '<td id="settings_category_name">test_category1</td>'.encode() in response.data
    assert '<td id="settings_category_description">test_category_1_description</td>'.encode() in response.data
    assert '''<form action="/budget/1/remove_category/1" onsubmit="return confirm('UWAGA! Wraz z usunięciem katetorii, usunięte zostaną wszystkie wpisy, do których przypisana została ta kategoria!\\nCzy na pewno chcesz usunąć tę kategorię?\\ntest_category1')"><button title="Usuń kategorię" class="remove_expense_btn" type="submit"><b>X</b></button></form>'''.encode() in response.data
    assert '<form><button title="Edytuj kategorię" class="remove_expense_btn" type="submit" formaction="/budget/1/edit_category/1"><b>&#9998</b></button></form>'.encode() in response.data

    assert '<td id="settings_category_color"><div style="background: #000000; min-height:20px; min-width:20px; margin:2px"></div></td>'.encode() in response.data
    assert '<td id="settings_category_name">test_category2</td>'.encode() in response.data
    assert '<td id="settings_category_description">test_category_2_description</td>'.encode() in response.data
    assert '''<form action="/budget/1/remove_category/2" onsubmit="return confirm('UWAGA! Wraz z usunięciem katetorii, usunięte zostaną wszystkie wpisy, do których przypisana została ta kategoria!\\nCzy na pewno chcesz usunąć tę kategorię?\\ntest_category2')"><button title="Usuń kategorię" class="remove_expense_btn" type="submit"><b>X</b></button></form>'''.encode() in response.data
    assert '<form><button title="Edytuj kategorię" class="remove_expense_btn" type="submit" formaction="/budget/1/edit_category/2"><b>&#9998</b></button></form>'.encode() in response.data

# ----------------------------
# '/budget/<int:budget_id>/add_category' TESTS
# ----------------------------

@pytest.mark.add_category
def test_add_category_get(client_logged_usr1):
    response = client_logged_usr1.get('/budget/1/add_category')
    assert '<div class="go_back_form"><a class="go_back_a" href="/budget/1/settings">< Wstecz</a></div>'.encode() in response.data
    
    assert '<td><label for="name">Nazwa kategorii</label></td>'.encode() in response.data
    assert '<td><input id="name" name="name" required type="text" value=""></td>'.encode() in response.data
    assert '<td><label for="description">Opis (opcjonalne)</label></td>'.encode() in response.data
    assert '<td><textarea id="description" name="description"></textarea></td>'.encode() in response.data
    assert '<td><label for="category_color">Kolor kategorii</label></td>'.encode() in response.data
    
    # Color field is filled by default with random generated Hex color value, that's why it needs regex for correct assertion
    regex = re.escape('<td><input id="category_color" name="category_color" required type="color" value="') + r"#(?:[0-9a-fA-F]{1,2}){3}" + re.escape('"></td>')
    assert re.search(regex, response.data.decode())

    assert '<td colspan="2" style="text-align: center;"><input id="submit" name="submit" type="submit" value="Wyślij"></td>'.encode() in response.data


@pytest.mark.add_category
def test_add_category_post(client_logged_usr1, app_ctx):
    form_data = {'name': 'test_post_category',
                'description': 'test post category description',
                'category_color': '#aaaaaa'
                }
    response = client_logged_usr1.post('/budget/1/add_category', data=form_data)
    assert response.status_code == 302

    new_category = Category.query.filter_by(name='test_post_category').first()
    assert new_category.id == 3
    assert new_category.name == 'test_post_category'
    assert new_category.description == 'test post category description'
    assert new_category.color == '#aaaaaa'


@pytest.mark.add_category
def test_add_category_post_empty(client_logged_usr1):
    form_data = {'name': '',
                'description': '',
                'category_color': ''
                }
    response = client_logged_usr1.post('/budget/1/add_category', data=form_data)
    assert response.status_code == 200

    assert 'Pole Nazwa nie może być puste.'.encode() in response.data
    assert 'Pole Kolor kategorii nie może być puste.'.encode() in response.data


@pytest.mark.add_category
def test_add_category_post_wrong_data(client_logged_usr1):
    form_data = {'name': 'test_post_category_wrong_data',
                'description': '',
                'category_color': '#23'
                }
    response = client_logged_usr1.post('/budget/1/add_category', data=form_data)
    assert response.status_code == 200

    assert '<td id="category_color_error">Kolor musi być podany w formacie HEX</td>'.encode() in response.data


# ----------------------------
# '/budget/<int:budget_id>/edit_category/<int:category_id>' TESTS
# ----------------------------

@pytest.mark.edit_category
def test_edit_category_get(client_logged_usr1):
    response = client_logged_usr1.get('/budget/1/edit_category/1')
    # response_to_file(response)
    assert '<div class="go_back_form"><a class="go_back_a" href="/budget/1/settings">< Wstecz</a></div>'.encode() in response.data

    assert '<td><label for="name">Nazwa kategorii</label></td>'.encode() in response.data
    assert '<td><input id="name" name="name" required type="text" value="test_category1"></td>'.encode() in response.data
    assert '<td><label for="description">Opis (opcjonalne)</label></td>'.encode() in response.data
    assert '<td><textarea id="description" name="description">test_category_1_description</textarea></td>'.encode() in response.data
    assert '<td><label for="category_color">Kolor kategorii</label></td>'.encode() in response.data
    assert '<td><input id="category_color" name="category_color" required type="color" value="#ffffff"></td>'.encode() in response.data
    assert '<td colspan="2" style="text-align: center;"><input id="submit" name="submit" type="submit" value="Zapisz"></td>'.encode() in response.data


@pytest.mark.edit_category
def test_edit_category_post(client_logged_usr1, app_ctx):
    form_data = {'name': 'test_edit_category_1',
                 'description': 'test edit category 1 description',
                 'category_color': '#aaaaaa'
                 }
    response = client_logged_usr1.post('/budget/1/edit_category/1', data=form_data)
    assert response.status_code == 302

    edited_category = Category.query.get(1)
    assert edited_category.id == 1
    assert edited_category.name == 'test_edit_category_1'
    assert edited_category.description == 'test edit category 1 description'
    assert edited_category.color == '#aaaaaa'


@pytest.mark.edit_category
def test_edit_category_post_empty(client_logged_usr1):
    form_data = {'name': '',
                 'description': '',
                 'category_color': ''
                 }
    response = client_logged_usr1.post('/budget/1/edit_category/1', data=form_data)
    assert response.status_code == 200

    assert 'Pole Nazwa nie może być puste.'.encode() in response.data
    assert 'Pole Kolor kategorii nie może być puste.'.encode() in response.data


@pytest.mark.edit_category
def test_edit_category_post_wrong_data(client_logged_usr1):
    form_data = {'name': 'test_edit_category_1',
                 'description': '',
                 'category_color': '#23'
                 }
    response = client_logged_usr1.post('/budget/1/edit_category/1', data=form_data)
    assert response.status_code == 200

    assert '<td id="category_color_error">Kolor musi być podany w formacie HEX</td>'.encode() in response.data


# ----------------------------
# '/budget/<int:budget_id>/remove_category/<int:category_id>' TESTS
# ----------------------------

@pytest.mark.remove_category
def test_remove_category_get(client_logged_usr1, app_ctx):
    all_expenses = len(Expense.query.all())
    expenses_cat2 = len(Expense.query.filter_by(category_id=2).all())

    all_used_by = len(UsedBy.query.all())
    used_by_cat_2 = len(UsedBy.query.filter(UsedBy.expense_id == Expense.id, Expense.category_id == 2).join(Expense).all())

    assert all_expenses == 7
    assert expenses_cat2 == 3
    assert all_used_by == 12
    assert used_by_cat_2 == 7


    response = client_logged_usr1.get('/budget/1/remove_category/2')

    all_expenses = len(Expense.query.all())
    expenses_cat2 = len(Expense.query.filter_by(category_id=2).all())
    all_used_by = len(UsedBy.query.all())
    used_by_cat_2 = len(UsedBy.query.filter(UsedBy.expense_id == Expense.id, Expense.category_id == 2).join(Expense).all())

    assert response.status_code == 302

    assert all_expenses == 4
    assert expenses_cat2 == 0
    assert all_used_by == 5
    assert used_by_cat_2 == 0


    response = client_logged_usr1.get('/budget/1/remove_category/2', follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == "/budget/1/settings"
