from flask import render_template, url_for

from main import app


@app.route('/')
def index():
    return render_template('main_page.html')


@app.route('/my_budgets')
def my_budgets():
    return render_template('my_budgets.html')