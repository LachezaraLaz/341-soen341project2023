#importing the sqlite3 module to handle database
import sqlite3
#importing Flask and other modules
from flask import Flask, request, render_template, redirect, session, Blueprint
from .signup import logout
#initializing blueprint
login = Blueprint('login', __name__)


# A decorator used to tell the application which URL is associated function
@login.route('/loginHTML.html', methods =['GET', 'POST'])
def loginFunc():
    if request.method == 'POST' and request.form.get("logout")!=None:
        logout()
        return render_template('home.html', boolean=True) 
    if request.method == 'POST':
       # getting input with name = fname in HTML form
       email = request.form.get("email")
       # getting input with name = lname in HTML form
       password = request.form.get("password")
       if (email == None):
          print("email is null")
       if (password == None):
          print("password is null")

       else:
          print(email + password)

          #connection to the database module
          conn = sqlite3.connect("data.db")
          # allow for SQL commands to be run
          c = conn.cursor()

          sqlComm1 = "SELECT * FROM LoginInfo WHERE email=\'"+email+"\'"
          row = c.execute(sqlComm1).fetchall()
          conn.commit()
          c.close()
          print(row)

          if (row == None):
             print("invalid login")
             return render_template('loginHTML.html', boolean=True)
          else:
             counter = 0
             userID = None
             userType = None 
             passwordMatch = False
             for x in row:
                userID = x[0]
                print(str(userID))
                if (x[2] == password):
                   passwordMatch = True
                userType = x[3]
                print(userType)
             
             if (passwordMatch == False):
                print("Incorrect password")
                return render_template('loginHTML.html', boolean=True)
             else:
                print("login successful")
                session["userID"] = userID
                session["email"] = email
                session["password"] = password
                session["userType"] = userType
                print(userType)
                if (userType == "student"):
                   return redirect("../indexCandidate.html")
                elif(userType == "admin"):
                   return redirect("../indexAdmin.html") 
                else:
                   return redirect("/indexEmployer.html")

    #if no POST request is made just stay on the login page
    return render_template('loginHTML.html', boolean=True)