from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField, SelectField, DateField, DecimalField, SelectMultipleField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, StopValidation
from wtforms.widgets import TableWidget, CheckboxInput
try:
    from wtforms.widgets import ColorInput
except ImportError:
    # The first method didn't work for pytest so here is workaround
    from wtforms.widgets import html5
    ColorInput = html5.ColorInput
from datetime import date

from script.models import User, Category, AllowedUsers


class MultiCheckboxField(SelectMultipleField):
    widget = TableWidget()
    option_widget = CheckboxInput()


class MultiCheckboxAtLeastOne():
    def __init__(self, message=None):
        if not message:
            message = 'At least one option must be selected.'
        self.message = message

    def __call__(self, form, field):
        if len(field.data) == 0:
            raise StopValidation(self.message)


class RegistrationForm(FlaskForm):
    username = StringField('Nazwa użytkownika', validators=[DataRequired("Pole Nazwa użytkownika nie może być puste.")])
    email = StringField('E-mail', validators=[DataRequired("Pole E-mail nie może być puste."), Email("Nieprawidłowy format adresu email.")])
    password = PasswordField('Hasło', validators=[DataRequired("Pole Hasło nie może być puste.")])
    password2 = PasswordField('Powtórz Hasło', validators=[DataRequired("Pole Powtórz Hasło nie może być puste."), EqualTo('password', "Hasła nie mogą się różnić.")])
    submit = SubmitField('Zarejestruj')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Ta nazwa użytkownika jest już zajęta. Proszę użyć innej nazwy użytkownika.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Ten adres email jest już zajęty. Proszę użyć innego adresu email.')

class LoginForm(FlaskForm):
    username = StringField('Nazwa użytkownika', validators=[DataRequired("Pole Nazwa użytkownika nie może być puste.")])
    password = PasswordField('Hasło', validators=[DataRequired("Pole Hasło nie może być puste.")])
    remember_me = BooleanField('Zapamiętaj mnie')
    submit = SubmitField('Zaloguj')

class BudgetForm(FlaskForm):
    name = StringField('Nazwa budżetu', validators=[DataRequired("Pole Nazwa budżetu nie może być puste.")])
    description = TextAreaField('Opis (opcjonalne)')
    submit = SubmitField('Wyślij')

class CategoryForm(FlaskForm):
    name = StringField('Nazwa kategorii', validators=[DataRequired()])
    description = TextAreaField('Opis (opcjonalne)')
    category_color = StringField('Kolor kategorii', widget=ColorInput())
    submit = SubmitField('Wyślij')

class ExpenseForm(FlaskForm):
    name = StringField('Nazwa', validators=[DataRequired()])
    description = TextAreaField('Opis (opcjonalne)')
    category = SelectField('Kategoria', choices=[])
    date = DateField('Data', format='%Y-%m-%d', validators=[DataRequired()])
    amount = DecimalField('Kwota', places=2, validators=[DataRequired()])
    payer = SelectField('Płaci', choices=[])
    used_by = MultiCheckboxField('Używa', choices=[], validators=[MultiCheckboxAtLeastOne()])
    submit = SubmitField('Wyślij')

    def validate_date(form, field):
        if field.data > date.today():
            raise ValidationError("Nie można użyć przyszłej daty")

    def get_categories(self, budget_id):
        categories = Category.query.filter_by(budget_id=budget_id).all()
        category_list = [cat.name for cat in categories]
        return category_list

    def get_allowed_users_names(self, budget_id):
        allowed_users = AllowedUsers.query.filter_by(budget_id=budget_id).all()
        allowed_users_list = [User.query.get(user.user_id).username for user in allowed_users]
        return allowed_users_list
        