#importing the sqlite3 module to handle database
import sqlite3
#importing Flask and other modules
from flask import Flask, request, render_template

#Flask constructor
loginFunctionality = Flask(__name__)

# A decorator used to tell the application which URL is associated function
@loginFunctionality.route('/loginHTML.html', methods =['GET', 'POST'])
def login():
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
          row = c.execute("SELECT userKey, email, password, userType from LoginInfo").fetchall()

          emailMatch = False
          passwordMatch = False
          userID = None
          userType = None
          rowCounter = 0
          trackRow = None

          for x in row:
            columnCounter = 0
            rowCounter += 1
            for y in x:
               columnCounter += 1
               print(y, end=' ')
               if (trackRow == None and columnCounter == 1):
                  userID = y
               if (columnCounter == 2):
                  if (email == y):
                     print("matching email!")
                     emailMatch = True
                     trackRow = rowCounter
               if (columnCounter == 3):
                  if (password == y):
                     print("matching password!")
                     passwordMatch = True
               if (rowCounter == trackRow and emailMatch == True and passwordMatch == True and columnCounter == 4):
                  userType = y
            print()

          conn.commit()
          c.close()
          
          if (passwordMatch == True and emailMatch == True):
             print("credentials valid, proceeding with login "+ str(userID) + " " + email + " " + password + " " + userType)
             if (userType == "student"):
                print("redirect to student profle")
             if (userType == "employer"):
                print("redirect to employer dashboard")
          else:
             print("incorrect login crendentials")
    return render_template('loginHTML.html', boolean=True)

if(__name__ == '__main__'):
    loginFunctionality.run(debug=True)