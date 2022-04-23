# FetchRewardsExercise

In order to run this application you need to have python 3. You can download at the following link https://www.python.org/downloads/release/python-3912/

1. Clone the repository onto your local machine
2. Create and activate a virtual environment
    1. Create: py -3 -m venv venv
    2. Activate: venv\Scripts\activate
3. Install:
    1. Flask: pip install flask
    2. flask-admin: pip install flask-admin
    3. SQL Alchemy: pip install flask-sqlalchemy
4. In the terminal type "flask run" in order to run the web app

* In order to view the available DB in the admin view go to "http://127.0.0.1:5000/admin"

- The first thing you will see is the main page with the title of the project along with a form where you can input (as the user) the amount of points that you want to use from your "account". The submit button sends that amount to a route in app.py where it subtracts the amount from the user and the payers. The balance route will show how many points each payer has left. 

- In the main page there are also 4 buttons under the form that add a set amount of points to your "account" when pressed. A new row is created in the payers table with the payers name, the points, and the timestamp of when those points were given.

- You can go back to the main page by going to "localhost:5000" in the search bar of the web browser.