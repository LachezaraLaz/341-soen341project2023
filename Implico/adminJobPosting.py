#importing the sqlite3 module to handle database
import sqlite3
#importing Flask and other modules
from flask import Flask, request, render_template, redirect, session, Blueprint
#initializing blueprint
adminJobPosting = Blueprint('adminJobPosting', __name__)

# A decorator used to tell the application which URL is associated function
@adminJobPosting.route('/viewJobPosting.html', methods =['GET', 'POST'])
def adminJobPostingFUNC():
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
                jpJobIDs[loopCounter] = column
            elif innerCounter == 1:
                jpUserIDS[loopCounter] = column
            elif innerCounter == 2:
                jpTitle[loopCounter] = column
            elif innerCounter == 3:
                jpCompany[loopCounter] = column
            elif innerCounter == 4:
                jpDescription[loopCounter] = column
            elif innerCounter == 5:
                jpRequirements[loopCounter] = column
            elif innerCounter == 6:
                jpLocation[loopCounter] = column
            elif innerCounter == 7:
                jpSalary[loopCounter] = column
            elif innerCounter == 8:
                jpCreationDate[loopCounter] = column
            elif innerCounter == 9:
                jpSelectedCandidate[loopCounter] = column
            innerCounter += innerCounter
        loopCounter += loopCounter
        

    conn.commit()
    c.close()
    return render_template('viewJobPosting.html', jobIDs = jpJobIDs, userIDs = jpUserIDS, jobTitle = jpTitle, jobDescription = jpDescription, jobRequirements = jpRequirements, jobLocation = jpLocation, jobSalary = jpSalary, jobCreationDate = jpCreationDate, jobSelectedCandidate = jpSelectedCandidate)