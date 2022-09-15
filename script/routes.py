from flask import render_template

from main import app


@app.route('/')
def index():
    return render_template('main_page.html')
