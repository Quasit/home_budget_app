from unicodedata import decimal
from flask import render_template, url_for, redirect, flash, request, g
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime, timedelta
from calendar import monthrange

from script.main import app, db, login_manager
from script.models import User, Budget, Category, Expense, AllowedUsers, UsedBy
from script.forms import RegistrationForm, LoginForm, BudgetForm, CategoryForm, ExpenseForm
from script.functions import (get_expenses, get_default_period_dates, get_expenses_from_period,
    get_expense_summary, random_color
)


@app.route('/')
def index():
    return render_template('main_page.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, virtual=False)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful, you can now log in.')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', form=form)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/my_budgets')
@login_required
def my_budgets():
    return render_template('my_budgets.html')


@app.route('/budget/add_budget', methods=['GET', 'POST'])
@login_required
def add_budget():
    form = BudgetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=current_user.id).first()
        budget = Budget(name=form.name.data, description=form.description.data, owner_id=user.id)
        db.session.add(budget)
        db.session.flush()
        allowedUser = AllowedUsers(budget_id=budget.id, user_id=user.id, editor=True)
        db.session.add(allowedUser)
        db.session.commit()
        return redirect(url_for('my_budgets'))
    return render_template('add_budget.html', form=form)


@app.route('/budget/<int:budget_id>')
@login_required
def budget(budget_id: int):
    budget = Budget.query.filter_by(id=budget_id).first()

    this_month_begin, this_month_end = get_default_period_dates('this_month')

    this_year_begin, this_year_end = get_default_period_dates('this_year')

    one_yar_period_begin, one_yar_period_end = get_default_period_dates('one_year')

    expenses_summary = {}

    # This month data
    all_this_month = get_expenses_from_period(budget_id, this_month_begin, this_month_end)
    expenses_summary["this_month"] = get_expense_summary(all_this_month)

    # This year data
    all_this_year = get_expenses_from_period(budget_id, this_year_begin, this_year_end)
    expenses_summary["this_year"] = get_expense_summary(all_this_year)

    # One year period data
    all_one_year_period = get_expenses_from_period(budget_id, one_yar_period_begin, one_yar_period_end)
    expenses_summary["one_year_period"] = get_expense_summary(all_one_year_period)

    return render_template('budget_summary.html', budget_id=budget.id, budget=budget, expenses_summary=expenses_summary)


@app.route('/budget/<int:budget_id>/expenses')
@login_required
def expenses(budget_id: int):
    budget = Budget.query.filter_by(id=budget_id).first()
    expenses = get_expenses(budget_id)
    return render_template('budget_expenses.html', budget_id=budget.id, budget=budget, expenses=expenses, counter=0)


@app.route('/budget/<int:budget_id>/add_expense', methods=['GET', 'POST'])
@login_required
def add_expense(budget_id: int):
    budget = Budget.query.filter_by(id=budget_id).first()
    form = ExpenseForm()
    form.category.choices = form.get_categories(budget_id)
    form.payer.choices = form.get_allowed_users_names(budget_id)
    form.used_by.choices = form.get_allowed_users_names(budget_id)
    if form.validate_on_submit():
        payer = User.query.filter_by(username=form.payer.data).first()
        category = Category.query.filter_by(budget_id=budget_id, name=form.category.data).first()
        expense = Expense(name=form.name.data, description=form.description.data,
                          budget_id=budget_id, category_id=category.id, date=form.date.data,
                          amount=str(form.amount.data), payer=payer.id)
        db.session.add(expense)
        db.session.flush()
        for user in form.used_by.data:
            used_by_user = User.query.filter_by(username=user).first()
            used_by_record = UsedBy(expense_id=expense.id, user_id=used_by_user.id)
            db.session.add(used_by_record)
        db.session.commit()
        return redirect(url_for('expenses', budget_id=budget_id))
    return render_template('add_expense.html', budget_id=budget_id, form=form)


@app.route('/budget/<int:budget_id>/edit_expense/<int:expense_id>', methods=['GET', 'POST'])
@login_required
def edit_expense(budget_id: int, expense_id: int):
    expense = Expense.query.filter_by(id=expense_id).first()
    database_used_by_records = UsedBy.query.filter_by(expense_id=expense_id).all()
    database_used_by_user_id = [record.user_id for record in database_used_by_records]
    form = ExpenseForm()
    form.category.choices = form.get_categories(budget_id)
    form.payer.choices = form.get_allowed_users_names(budget_id)
    form.used_by.choices = form.get_allowed_users_names(budget_id)
    if form.validate_on_submit():
        # Expense table changes
        category = Category.query.filter_by(budget_id=budget_id, name=form.category.data).first()
        expense.name = form.name.data
        expense.description = form.description.data
        expense.category_id = category.id
        expense.date = form.date.data
        expense.amount = str(form.amount.data)
        expense.payer = User.query.filter_by(username=form.payer.data).first().id
        # UsedBy table changes
        # First change username from form field to userId list
        form_used_by_user_id = [User.query.filter_by(username=user).first().id for user in form.used_by.data]
        # Then need to delete sql records which should be removed and update list
        for record in database_used_by_user_id:
            if record not in form_used_by_user_id:
                record_to_remove = UsedBy.query.filter_by(user_id=record).first()
                db.session.delete(record_to_remove)
                database_used_by_user_id.remove(record)
        # Then we need to update our
        for record in form_used_by_user_id:
            if record not in database_used_by_user_id:
                new_record = UsedBy(expense_id=expense.id, user_id=record)
                db.session.add(new_record)
        db.session.commit()
        return redirect(url_for('expenses', budget_id=budget_id))
    form.submit.label.text = "Zapisz"
    form.category.choices = form.get_categories(budget_id)
    category = Category.query.filter_by(id=expense.category_id).first()
    form.category.default = category.name
    form.process()
    form.name.data = expense.name
    form.description.data = expense.description
    form.amount.data = float(expense.amount)
    form.date.data = expense.date
    form.payer.data = User.query.get(expense.payer).username
    used_by_list = [User.query.filter_by(id=record.user_id).first().username for record in database_used_by_records]
    form.used_by.data = used_by_list
    return render_template('edit_expense.html', budget_id=budget_id, form=form, expense_id=expense_id, expense=expense)


@app.route('/budget/<int:budget_id>/remove_expense/<int:expense_id>')
def remove_expense(budget_id: int, expense_id: int):
    expense_to_remove = Expense.query.filter_by(id=expense_id).first()
    used_by_records = UsedBy.query.filter_by(expense_id=expense_to_remove.id).all()
    db.session.delete(expense_to_remove)
    for record in used_by_records:
        db.session.delete(record)
    db.session.commit()
    return redirect(url_for('expenses', budget_id=budget_id))


@app.route('/budget/<int:budget_id>/add_category', methods=['GET', 'POST'])
@login_required
def add_category(budget_id: int):
    budget = Budget.query.filter_by(id=budget_id).first()
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(name=form.name.data, description=form.description.data, budget_id=budget_id, color=form.category_color.data)
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('budget_settings', budget_id=budget_id))
    form.category_color.data = random_color()
    return render_template('add_category.html', budget_id=budget_id, form=form)


@app.route('/budget/<int:budget_id>/edit_category/<int:category_id>', methods=['GET', 'POST'])
@login_required
def edit_category(budget_id: int, category_id: int):
    budget = Budget.query.filter_by(id=budget_id).first()
    category = Category.query.filter_by(id=category_id).first()
    form = CategoryForm()
    if form.validate_on_submit():
        category.name = form.name.data
        category.description = form.description.data
        category.color = form.category_color.data
        db.session.commit()
        return redirect(url_for('budget_settings', budget_id=budget_id))
    form.submit.label.text = "Zapisz"
    form.process()
    form.name.data = category.name
    form.description.data = category.description
    form.category_color.data = category.color
    return render_template('edit_category.html', budget_id=budget_id, form=form)


@app.route('/budget/<int:budget_id>/remove_category/<int:category_id>')
def remove_category(budget_id: int, category_id: int):
    category_to_remove = Category.query.filter_by(id=category_id).first()
    db.session.delete(category_to_remove)
    db.session.commit()
    return redirect(url_for('budget_settings', budget_id=budget_id))


@app.route('/budget/<int:budget_id>/settings')
def budget_settings(budget_id: int):
    budget = Budget.query.filter_by(id=budget_id).first()
    categories = Category.query.filter_by(budget_id=budget_id).all()
    return render_template('budget_settings.html', budget=budget, budget_id=budget_id, categories=categories)


@app.route('/testing')
def testing():
    return render_template('testing.html')


@app.route('/test')
def test():
    return render_template('test.html')
