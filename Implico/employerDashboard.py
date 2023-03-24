#importing the sqlite3 module to handle database
import sqlite3
import datetime
#importing Flask and other modules
from flask import Flask, request, render_template, redirect, session, Blueprint
#initializing blueprint
employerDashboard = Blueprint('employerDashboard', __name__)

@employerDashboard.route('viewMoreJobEmployer.html', methods =['GET', 'POST'])
def func1():
    return

@employerDashboard.route('/jobDashboardHTML.html', methods = ['GET','POST'])
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
            return redirect('/jobDashboardHTML.html')
        elif 'Add' in request.form:
            return redirect("/editJobPosting.html")
        # edit button functionality
        elif(request.form.get("editPostingID") != None):
            session["editPostingID"] = request.form["editPostingID"]
            print("session id is", session["editPostingID"])
            return redirect("/editJobPosting.html")

@employerDashboard.route("/editJobPosting.html",methods = ['GET','POST'])
def editPosting():
    # not logged in or not redirected from edit posting page
    if request.method == 'GET' and (session.get("userID") == None):
        print("here 1")
        return redirect("/loginHTML.html")
    elif request.method == 'GET' and session.get("userID") != None and session.get("editPostingID") != None:
        print("here 2")
        # all good to load (logged in and editposting id set)
        conn = sqlite3.connect("data.db")
        c = conn.cursor()
        jobPosting = c.execute("SELECT * FROM JobPostings WHERE jobKey=" + session["editPostingID"]).fetchone()
        print(jobPosting)
        return render_template("/editJobEmployer.html", title = jobPosting[2], company = jobPosting[3], description = jobPosting[4], requirements = jobPosting[5], location = jobPosting[6], salary = jobPosting[7])
    elif request.method == 'GET' and session.get("userID") != None:
        return render_template("/editJobEmployer.html")
    elif request.method == 'POST' and session.get("editPostingID") != None:
        print("here 3")
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
    elif request.method == "POST" and session.get("userID") != None:
        print("here 4")
        # New table record
        conn = sqlite3.connect("data.db")
        c = conn.cursor()
        userID = session["userID"]
        title = request.form["jobTitle"]
        company = request.form["company"]
        jobDescription = request.form["jobDescription"]
        jobRequirements = request.form["jobRequirements"]
        jobLocation = request.form["jobLocation"]
        salary= request.form["salary"]
        timeNow = datetime.datetime.now()
        timeNowFormatted = timeNow.strftime("%Y-%m-%d-%X")
        lastKey = c.execute("SELECT jobKey FROM JobPostings ORDER BY jobKey DESC LIMIT 1").fetchone()[0]
        print(lastKey)
        newEntry = "INSERT INTO JobPostings VALUES ('" + str(lastKey+1) + "','" + str(userID) + "','" + str(title) + "','" + str(company) + "','" + str(jobDescription) + "','" + str(jobRequirements) + "','" + str(jobLocation) + "','" + str(salary) + "','" + str(timeNowFormatted) + "','None')"
        c.execute(newEntry)
        conn.commit()
        c.close()
        return redirect("/jobDashboardHTML.html")

@employerDashboard.route("/app")
def jobApp():
    return render_template("/jobApplicantsEmployer.html")