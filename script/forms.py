from logging.config import valid_ident
from unicodedata import category, name
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField, SelectField, DateField, DecimalField, SelectMultipleField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, InputRequired

from models import User, Category


class RegistrationForm(FlaskForm):
    username = StringField('Nazwa użytkownika', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    password2 = PasswordField('Powtórz Hasło', validators=[DataRequired(), EqualTo('password')])
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
    username = StringField('Nazwa użytkownika', validators=[DataRequired()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    remember_me = BooleanField('Zapamiętaj mnie')
    submit = SubmitField('Zaloguj')

class BudgetForm(FlaskForm):
    name = StringField('Nazwa budżetu', validators=[DataRequired()])
    description = TextAreaField('Opis (opcjonalne)')
    submit = SubmitField('Wyślij')

class CategoryForm(FlaskForm):
    name = StringField('Nazwa kategorii', validators=[DataRequired()])
    description = TextAreaField('Opis (opcjonalne)')
    submit = SubmitField('Wyślij')

class ExpenseForm(FlaskForm):
    name = StringField('Nazwa', validators=[DataRequired()])
    description = TextAreaField('Opis (opcjonalne)')
    category = SelectField('Kategoria', choices=[])
    date = DateField('Data', format='%Y-%m-%d', validators=[DataRequired()])
    amount = DecimalField('Kwota', places=2, validators=[DataRequired()])
    #payer = SelectField('Płaci', choices=[])
    #used_by = SelectMultipleField('Używa', choices=[])
    submit = SubmitField('Wyślij')

    def get_categories(self, budget_id):
        categories = Category.query.filter_by(budget_id=budget_id).all()
        category_list = [cat.name for cat in categories]
        return category_list