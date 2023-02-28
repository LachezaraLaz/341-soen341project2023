#importing the sqlite3 module to handle database
import sqlite3
#importing Flask and other modules
from flask import Flask, request, render_template, redirect, url_for, session

#Flask constructor
loginFunctionality = Flask(__name__)

loginFunctionality.secret_key = "some_secret_key"

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
          #retrieve the information from the LoginInfo database table
          row = c.execute("SELECT userKey, email, password, userType from LoginInfo").fetchall()

          #initalizing the variables for the upcoming for loop
          emailMatch = False
          passwordMatch = False
          userID = None
          userType = None
          rowCounter = 0
          trackRow = None

          #for loop which parses through the data from the logginInfo databaase table previosuly fetched,
          #and compares it with the login credentials inputted by the user from the lognHTML.html frontend page
          for x in row:
            #reset the column tracker back to the beginning eaach time we move down a row in the database table
            columnCounter = 0
            #increment the row counter to match the actual row we are iterating over in the database table
            rowCounter += 1
            for y in x:
               #update column counter with every iteration on the row
               columnCounter += 1
               print(y, end=' ')
               #if we are iterating over the user ID column, and if we have not yet found any row with a matching email, update the userID
               if (trackRow == None and columnCounter == 1):
                  userID = y
               #if we are iterating over the email column
               if (columnCounter == 2):
                  #if the emails match then change emailMatch bolean to True and keep track of which row the match occurred in
                  if (email == y):
                     print("matching email!")
                     emailMatch = True
                     trackRow = rowCounter
               #if we are iterating over the password column and we are in a row where the emails have matched
               if (trackRow == rowCounter and columnCounter == 3):
                  #if the passwords match change passwordMatch boolean to true
                  if (password == y):
                     print("matching password!")
                     passwordMatch = True
               #if we are in a row where the emails match and the passwords match, and oteraatiing over the user type column
               if (rowCounter == trackRow and emailMatch == True and passwordMatch == True and columnCounter == 4):
                  #assign userType to the current value we retrieved while iterating
                  userType = y
            print()

          conn.commit()
          c.close()
          
          #if the login is valid then session is created with session variables containing user login info and redirected either
          # to profile page or dashboard depending on user type
          if (passwordMatch == True and emailMatch == True):
             print("credentials valid, proceeding with login "+ str(userID) + " " + email + " " + password + " " + userType)
             session["userID"] = userID
             session["email"] = email
             session["password"] = password
             session["userType"] = userType
             if (userType == "student"):
                print("redirect to student profile")
                return redirect(url_for("profileHTML.html"))
             if (userType == "employer"):
                print("redirect to employer dashboard")
                return redirect(url_for("dashboardHTML.html"))
          #if login is invalid you just stay on login page and no session is created
          else:
             print("incorrect login crendentials")
             return render_template('loginHTML.html')
    #if no POST request is made just stay on the login page
    return render_template('loginHTML.html', boolean=True)

if(__name__ == '__main__'):
    loginFunctionality.run(debug=True)