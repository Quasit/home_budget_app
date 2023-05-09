from script.models import User


# CURRENT ROUTES
# '/' - DONE
# '/register' - DONE
# '/login' - DONE
# '/logout' - DONE
# '/my_budgets' - DONE
# '/budget/add_budget'
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

def test_base_index(client):
    response = client.get('/')
    assert "Strona główna".encode() in response.data


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
    response_usr1 = client_logged_usr1.get('/')
    assert b"test_budget_1" in response_usr1.data
    assert b"test_budget_2" not in response_usr1.data


def test_get_allowed_budgets_usr2(client_logged_usr2):
    # User 2 should see test_budget_1 and test_budget_2
    response_usr2 = client_logged_usr2.get('/')
    assert b"test_budget_1" in response_usr2.data
    assert b"test_budget_2" in response_usr2.data


# ----------------------------
# '/register' TESTS
# ----------------------------

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


def test_register_post_empty_data(client):
    error_tr = '<tr class="register_errors">\n                    <td></td>\n                    <td>Pole nie może być puste.</td>'
    username_err = '<input id="username" name="username" required size="32" type="text" value=""></td>\n                </tr>\n                \n                ' + error_tr
    email_err = '<input id="email" name="email" required size="32" type="text" value=""></td>\n                </tr>\n                \n                ' + error_tr
    password_err = '<input id="password" name="password" required size="32" type="password" value=""></td>\n                </tr>\n                \n                ' + error_tr
    password2_err = '<input id="password2" name="password2" required size="32" type="password" value=""></td>\n                </tr>\n                \n                ' + error_tr
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

def test_login_get(client):
    response = client.get('/login')
    assert '<label for="username">Nazwa użytkownika</label>'.encode() in response.data
    assert '<input id="username" name="username" required size="32" type="text" value="">'.encode() in response.data
    assert '<label for="password">Hasło</label>'.encode() in response.data
    assert '<input id="password" name="password" required size="32" type="password" value="">'.encode() in response.data
    assert '<label for="remember_me">Zapamiętaj mnie</label>'.encode() in response.data
    assert '<input id="remember_me" name="remember_me" type="checkbox" value="y">'.encode() in response.data
    assert '<input id="submit" name="submit" type="submit" value="Zaloguj">'.encode() in response.data


def test_login_post(client):
    form_data = {'username': 'test_post_username',
                 'password': 'testpostpassword',
                 'remember_me' : False
                 }
    response = client.post('/login', data=form_data)
    assert response.status_code == 302


def test_login_post_redirect(client):
    form_data = {'username': 'test_user',
                 'password': 'test',
                 'remember_me': False
                 }
    response = client.post('/login', data=form_data, follow_redirects=True)
    assert response.status_code == 200
    assert b"Wyloguj" in response.data


def test_login_post_wrong_username(client):
    form_data = {'username': 'wrong_username',
                 'password': 'test',
                 'remember_me': False
                 }
    response = client.post('/login', data=form_data, follow_redirects=True)
    assert response.status_code == 200
    assert '<p class="flashes">\n        \n        Invalid username or password\n        \n    </p>'.encode() in response.data


def test_login_post_wrong_password(client):
    form_data = {'username': 'test_user',
                 'password': 'wrong_password',
                 'remember_me': False
                 }
    response = client.post('/login', data=form_data, follow_redirects=True)
    assert response.status_code == 200
    assert '<p class="flashes">\n        \n        Invalid username or password\n        \n    </p>'.encode() in response.data


def test_login_post_empty_data(client):
    error_tr = '<tr class="login_errors">\n                    <td></td>\n                    <td>Pole nie może być puste.</td>'
    username_err = '<input id="username" name="username" required size="32" type="text" value=""></td>\n                </tr>\n                \n                ' + error_tr
    password_err = '<input id="password" name="password" required size="32" type="password" value=""></td>\n                </tr>\n                \n                ' + error_tr
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

def test_logout(client_logged_usr1):
    response = client_logged_usr1.get('/')
    assert b"Wyloguj" in response.data
    response = client_logged_usr1.get('/logout', follow_redirects=True)
    assert b"Zaloguj" in response.data


# ----------------------------
# '/my_budgets' TESTS
# ----------------------------

def test_my_budgets_route(client_logged_usr1):
    response_usr1 = client_logged_usr1.get('/my_budgets')
    assert b"test_budget_1</a> - test_budget_1_description</h3>" in response_usr1.data
    assert b"test_budget_2</a> - test_budget_2_description</h3>" not in response_usr1.data


def test_my_budgets_route(client_logged_usr2):
    response_usr2 = client_logged_usr2.get('/my_budgets')
    assert b"test_budget_1</a> - test_budget_1_description</h3>" in response_usr2.data
    assert b"test_budget_2</a> - test_budget_2_description</h3>" in response_usr2.data


# ----------------------------
# '/budget/add_budget' TESTS
# ----------------------------

def test_add_budget_get(client_logged_usr1):
    pass
    # response = client_logged_usr1.get('/budget/add_budget')
    # print(response.data)
    # assert False
