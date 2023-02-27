#
import sqlite3
#importing Flask and other modules
from flask import Flask, request, render_template

#Flask constructor
loginFunctionality = Flask(__name__)

# A decorator used to tell the application which URL is associated function
@loginFunctionality.route('/login.html', methods =["GET", "POST"])
def login():
    if request.method == "POST":
       # getting input with name = fname in HTML form
       email = request.form.get("email")
       # getting input with name = lname in HTML form
       password = request.form.get("password")
       print(email + password)
       return "Your email is "+ email + "Your password is "+ password
    return render_template('login.html', boolean=True)

if(__name__ == '__main__'):
    loginFunctionality.run(debug=True)