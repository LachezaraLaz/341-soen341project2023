# import database to connect and manage database
# flask to use Flask framework and
# request to handle HTML form requests
import sqlite3
from flask import Flask, request, render_template, Blueprint, redirect
#initializing Blueprint
signup = Blueprint('signup', __name__)

#map route to signup  URL (tells Flask what URL triggers our following functions)
@signup.route('/signUpHTML.html',methods = ['POST','GET'])
def signupFunc():
    if request.method == "GET":
        return render_template('signUpHTML.html')
    elif request.method == "POST":
        # fetch email and password from form
        email = request.form['email']
        password = request.form['password']
        userType = request.form.get('userType')
        print("email is ",email)
        print("password is ", password)
        print(str(email[0:email.index("@")]),"hi")

        # connection to the database module
        conn = sqlite3.connect("data.db")
        c = conn.cursor()

        # Verify that the user doesn't already exist
        checkUser = "SELECT email FROM LoginInfo WHERE email =\'" + str(email) + "\'"
        userExists = c.execute(checkUser).fetchone()
        if(userExists != None):
            return "user already exists"

        # If user doesn't exist, add them to the database
        lastKey = c.execute("SELECT userKey FROM LoginInfo ORDER BY userKey DESC LIMIT 1").fetchone()[0]
        print("Key inside:",lastKey)

        # fetch row and store new record
        row = c.execute("SELECT userKey, email, password FROM LoginInfo").fetchall()
        lastKey = c.execute("SELECT userKey FROM LoginInfo ORDER BY userKey DESC").fetchone()[0]
        newUser = "INSERT INTO LoginInfo VALUES (" + str(lastKey+1) + ",\'" + str(email) + "\',\'" + str(password) + "\',\'" + str(userType) + "\')"

        # Create new user profile
        if(userType == "student"):
            lastProfileKey = c.execute("SELECT profileKey FROM UserProfiles ORDER BY profileKey DESC LIMIT 1").fetchone()[0]
            newProfile = "INSERT INTO UserProfiles (profileKey, userID) VALUES (" + str(lastProfileKey+1) +"," + str(lastKey+1) + ")"
            c.execute(newProfile)
        c.execute(newUser)
        conn.commit()
        c.close()
        return redirect('../loginHTML.html')

@signup.route('/jobPostings.html',methods = ['POST','GET'])
def jobPostings():
    if request.method == 'GET':
        return render_template('jobPostingHTML.html')
    elif request.method == 'POST':
        companyName = request.form['companyName']
        positionName = request.form['positionName']
        location = request.form['location']
        workMode = request.form['workMode']
        salary = request.form['salary']
        contactFName = request.form['contactFName']
        contactLName = request.form['contactLName']
        contactEmail = request.form['contactEmail']
        description = request.form['description']
    
    # Need to fetch posting ID to continue <--------------

@signup.route('/jobDashboardHTML.html')
def jobDashboard():
     # connection to the database module
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    jobPostings = c.execute("SELECT * FROM JobPostings").fetchall()
    print(jobPostings)
    return render_template("jobDashboardHTML.html", jobPostings = jobPostings)
