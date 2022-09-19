from flask import render_template, url_for

from main import app


@app.route('/')
def index():
    return render_template('main_page.html')


@app.route('/my_budgets')
def my_budgets():
    return render_template('my_budgets.html')


@app.route('/budget/<int:id>')
def budget(id: int):
    return render_template('budget_page.html', id=id)


@app.route('/testing')
def testing():
    return render_template('testing.html')
