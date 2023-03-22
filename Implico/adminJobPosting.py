#importing the sqlite3 module to handle database
import sqlite3
#importing Flask and other modules
from flask import Flask, request, render_template, redirect, session, Blueprint
#initializing blueprint
adminJobPosting = Blueprint('adminJobPosting', __name__)

# A decorator used to tell the application which URL is associated function
@adminJobPosting.route('/adminJobDashboard.html', methods =['GET', 'POST'])
def adminJobPostingFUNC():
    if session["userID"] != 5:
        #send the user back to login page if they are not the admin user
        return redirect("../loginHTML.html")
    elif request.method == 'GET':
        #connection to the database module
        conn = sqlite3.connect("data.db")
        # allow for SQL commands to be run
        c = conn.cursor()
        
        sqlComm1 = "SELECT * FROM JobPostings"
        row = c.execute(sqlComm1).fetchall()
        print(row)

        #retrieving all the data in the jobPosting table and putting it into arrays
        jpJobIDs = []
        jpUserIDS = []
        jpTitle = []
        jpCompany = []
        jpDescription = []
        jpRequirements = []
        jpLocation = []
        jpSalary = []
        jpCreationDate = []
        jpSelectedCandidate = []

        loopCounter = 0
        for jobPosting in row:
            innerCounter =  0
            for column in jobPosting:
                if innerCounter == 0:
                    jpJobIDs.append(column)
                elif innerCounter == 1:
                    jpUserIDS.append(column)
                elif innerCounter == 2:
                    jpTitle.append(column)
                elif innerCounter == 3:
                    jpCompany.append(column)
                elif innerCounter == 4:
                    jpDescription.append(column)
                elif innerCounter == 5:
                    jpRequirements.append(column)
                elif innerCounter == 6:
                    jpLocation.append(column)
                elif innerCounter == 7:
                    jpSalary.append(column)
                elif innerCounter == 8:
                    jpCreationDate.append(column)
                elif innerCounter == 9:
                    jpSelectedCandidate.append(column)
                innerCounter = innerCounter + 1
            loopCounter = loopCounter + 1
            

        conn.commit()
        c.close()
        return render_template('adminJobDashboard.html', counter = loopCounter, jobIDs = jpJobIDs, userIDs = jpUserIDS, jobCompany = jpCompany, jobTitle = jpTitle, jobDescription = jpDescription, jobRequirements = jpRequirements, jobLocation = jpLocation, jobSalary = jpSalary, jobCreationDate = jpCreationDate, jobSelectedCandidate = jpSelectedCandidate)
    elif request.method == 'POST':
        return redirect("../adminJobDashboard.html")