# import database to connect and manage database
# flask to use Flask framework and
# request to handle HTML form requests
import sqlite3
from flask import Flask, request, render_template, Blueprint, redirect, session
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

@signup.route('/dashboard', methods = ['GET','POST'])
def jobDashboard():
    if request.method == 'GET':
        # connection to the database module
        conn = sqlite3.connect("data.db")
        c = conn.cursor()
        jobPostings = c.execute("SELECT * FROM JobPostings").fetchall()
        return render_template("jobDashboardHTML.html", jobPostings = jobPostings)
    elif request.method == 'POST':
        conn = sqlite3.connect("data.db")
        c = conn.cursor()
        # delete button functionality
        if (request.form.get("deletePostingID") != None):
            print(str(request.form.get("deletePostingID")))
            deleteQuery = "DELETE FROM JobPostings WHERE jobKey=" + str(request.form.get("deletePostingID"))
            c.execute(deleteQuery)
            conn.commit()
            c.close()
            return redirect('/dashboard')
        elif (request.form.get("addPostingID") != None):
            return "abc"
        # edit button functionality
        elif(request.form.get("editPostingID") != None):
            session["editPostingID"] = request.form["editPostingID"]
            print("session id is", session["editPostingID"])
            return redirect("/editJobPosting.html")
        
@signup.route("/editJobPosting.html",methods = ['GET','POST'])
def editPosting():
    # not logged in or not redirected from edit posting page
    if request.method == 'GET' and (session.get("userID") == None or session.get("editPostingID")== None):
        return redirect("/loginHTML.html")
    elif request.method == 'GET' and session.get("userID") != None and session.get("editPostingID") != None:
        # all good to load (logged in and editposting id set)
        conn = sqlite3.connect("data.db")
        c = conn.cursor()
        jobPosting = c.execute("SELECT * FROM JobPostings WHERE jobKey=" + session["editPostingID"]).fetchone()
        print(jobPosting)
        return render_template("/editJobEmployer.html", title = jobPosting[2], company = jobPosting[3], description = jobPosting[4], requirements = jobPosting[5], location = jobPosting[6], salary = jobPosting[7])
    elif request.method == 'POST':
        # update existing table record
        conn = sqlite3.connect("data.db")
        c = conn.cursor()
        editPostingID = session["editPostingID"]
        title = request.form["jobTitle"]
        company = request.form["company"]
        jobDescription = request.form["jobDescription"]
        jobRequirements = request.form["jobRequirements"]
        jobLocation = request.form["jobLocation"]
        salary= request.form["salary"]
        updateQuery = "UPDATE JobPostings SET title ='" + str(title) + "',company='" + str(company) + "',jobDescription='" + str(jobDescription) + "',requirements='" + str(jobRequirements) + "',workLocation='" + str(jobLocation) + "',salary='" + str(salary) + "'WHERE jobKey=" + str(editPostingID)
        c.execute(updateQuery)
        conn.commit()
        c.close()
        session.pop("editPostingID",None)
        return redirect("/dashboard")
    
@signup.route("/app")
def jobApp():
    return render_template("/jobApplicantsEmployer.html")

@signup.route("/VUJP",methods = ['GET','POST'])
def viewPosting():
    if request.method == 'GET' and (session.get("userID") == None):
        return redirect("/loginHTML.html")
    if request.method == 'GET':
        # connection to the database module
        conn = sqlite3.connect("data.db")
        c = conn.cursor()
        jobPostings = c.execute("SELECT * FROM JobPostings").fetchall()
        return render_template("/viewJobPosting.html",  jobPostings = jobPostings)
  