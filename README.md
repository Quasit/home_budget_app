<a name="readme-top"></a>
<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Quasit/home_budget_app">
    <img src="static/images/logo_60x60.png" alt="Logo" width="60" height="60">
  </a>

  <h3 align="center">Home budget app</h3>

  <p align="center">
    Flask app project for home budget management.
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#installation">Installation</a>
    </li>
    <li><a href="#features">Features</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

![Early preview picture](static/images/early_preview.jpeg)

This is my personal project to develop my coding skills around Flask framework.

Project is still under development

The main idea was to build web app for management home budget with more than 1 person.
The app's main use is to add all expenses and incomes made by all persons included in budget, but also check which person is using those expenses.
For example when there is 2 people in house and one buys dinner, but both of them are using it. But the other time one of those persons buys ice cream and eats it alone.
And this app is meant to allow to check who is using how much from money spent and how much money is spent compared to income.


<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

Below are major frameworks/libraries that I used to build that project 

* Python 3
* Flask
* Jinja2 templates (HTML)
* SQLAlchemy
* SQLite
* Javascript
* Pytest


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- Installation -->
## Installation

To run application locally follow below steps

1. Clone the repo
   ```sh
   git clone https://github.com/Quasit/home_budget_app.git
   ```
2. Create venv
    ```sh
    python -m venv .venv
    ```
3. Install requirements
   ```sh
   pip install requirements.txt
   ```
4. Create `config.py` in /script folder and fill it up as below:
   ```python
    class DevelopmentConfig():
        TESTING = False
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        SECRET_KEY = 'ENTER YOUR SECRET KEY'
        SQLALCHEMY_DATABASE_URI = 'sqlite:///../budget_database.db'
   ```
5. Run app in development mode:
   ```sh
   $env:FLASK_ENV="development"; python3 app_run.py
   ```
6. App is available in your browser at 127.0.0.1:5000/


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- IMPLEMENTED FEATURES -->
## FEATURES

Below are listed features that I have already implemented in the project

* User Registering and Logging
* CRUD and Database models
* Data forms with input validation
* Special input types in forms
  * Date with Calendar popup
  * Color with Color Picker
* Data visualization in charts
* Unit Tests


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [x] Base templates
- [x] SQLite database and SQLAlchemy Models
- [x] User register and login system and pages
- [x] Basic Budget pages
- [x] Basic Expenses pages
- [ ] Basic Income pages
- [x] Expenses and income list in table page
- [x] Pagination in Expenses and Income table page
- [ ] Filters in Expenses and Income table page
- [x] Summary view for basic periods (current month / current year / one year period)
- [ ] Summary view for user selected dates
- [x] Basic chart in budget summary page
- [ ] Page with additional charts
- [x] Color picker for Expenses Categories
- [ ] Adding other Users to Budgets in Budget settings page
- [x] Pytest fixtures and test database prep
- [x] Unit tests for app and database setup
- [ ] Unit tests for functions
- [ ] Unit tests for routes


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Email - waltermichal92@gmail.com

Project Link: [Home Budget App](https://github.com/Quasit/home_budget_app)


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

I would like to give credit to scripts, that I used to make my project better.

* [Chart.js](https://www.chartjs.org/)
* [w3schools](https://www.w3schools.com/)


<p align="right">(<a href="#readme-top">back to top</a>)</p>