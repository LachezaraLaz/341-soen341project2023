#python file for all admin functionalities
#importing the sqlite3 module to handle database
import sqlite3
#importing Flask and other modules
from flask import Flask, request, render_template, redirect, session, Blueprint
#initializing blueprint
adminPages = Blueprint('adminPages', __name__)

# A decorator used to tell the application which URL is associated function
@adminPages.route('/adminJobDashboard.html', methods =['GET', 'POST'])
def adminJobPostingFUNC():
    if request.method == 'POST' and request.form.get("logout")!=None:
        session.pop("userID", None)
        session.pop("email", None)
        session.pop("password", None)
        session.pop("userType", None)
        return render_template('home.html', boolean=True) 
    elif session["userID"] != 5:
        #send the user back to login page if they are not the admin user
        return redirect("../loginHTML.html")
    elif request.method == 'GET':
        #connection to the database module
        conn = sqlite3.connect("data.db")
        # allow for SQL commands to be run
        c = conn.cursor()
        
        sqlComm1 = "SELECT * FROM JobPostings"
        row = c.execute(sqlComm1).fetchall()

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
                    jpDescription.append(shortenString(column))
                elif innerCounter == 5:
                    jpRequirements.append(shortenString(column))
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
         deleteJobID = request.form.get("deleteJobID")
         print(deleteJobID)
         editJobID = request.form.get("editJobID")
         print(editJobID)
         if (deleteJobID != None):
            deleteJob = request.form.get("deleteJobID")
            print(deleteJob)

            #connection to the database module
            conn = sqlite3.connect("data.db")
            # allow for SQL commands to be run
            c = conn.cursor()
                
            sqlComm1 = "DELETE FROM JobPostings WHERE jobKey = "+deleteJob
            row = c.execute(sqlComm1).fetchall()

            conn.commit()
            c.close()

            return redirect("../adminJobDashboard.html")
         elif (editJobID != None):
            editJobID = request.form.get("editJobID")
            print(editJobID)
            
            session['editJobID'] = editJobID

            return redirect('../editJobAdmin.html')
        
# A decorator used to tell the application which URL is associated function
@adminPages.route('/editJobAdmin.html', methods =['GET', 'POST'])
def adminEditJobFUNC():
    if request.method == 'POST' and request.form.get("logout")!=None:
        session.pop("userID", None)
        session.pop("email", None)
        session.pop("password", None)
        session.pop("userType", None)
        return render_template('home.html', boolean=True) 
    elif request.method == 'GET':
        editJobID = session['editJobID']
        print(editJobID)
        #connection to the database module
        conn = sqlite3.connect("data.db")
        # allow for SQL commands to be run
        c = conn.cursor()
            
        sqlComm1 = "SELECT * FROM JobPostings WHERE jobKey = "+str(editJobID)
        row = c.execute(sqlComm1).fetchall()
        print(row)

        conn.commit()
        c.close()

        editJob = []
        for x in row[0]:
            print("looping")
            editJob.append(x)
        print(editJob)
        jobTitle = editJob[2]
        jobCompany = editJob[3]
        jobDescription = editJob[4]
        jobRequirements = editJob[5]
        jobLocation = editJob[6]
        jobSalary = editJob[7]
        return render_template('editJobAdmin.html', jobTitle = jobTitle, jobCompany = jobCompany, jobDescription = jobDescription, jobRequirements = jobRequirements, jobLocation = jobLocation, jobSalary = jobSalary)
    if request.method == 'POST':
        jobID = session['editJobID']
        jobTitle = request.form.get("jobTitle")
        jobCompany = request.form.get("jobCompany")
        jobDescription = request.form.get("jobDescription")
        jobRequirements = request.form.get("jobRequirements")
        jobCompany = request.form.get("jobCompany")
        jobLocation = request.form.get("jobLocation")
        jobSalary = request.form.get("jobSalary")

        conn = sqlite3.connect("data.db")
        # allow for SQL commands to be run
        c = conn.cursor()
            
        sqlComm1 = "UPDATE JobPostings SET title = '"+str(jobTitle)+"', company = '"+str(jobCompany)+"', jobDescription = '"+str(jobDescription)+"', requirements = '"+str(jobRequirements)+"', workLocation = '"+str(jobLocation)+"', salary = '"+str(jobSalary)+"'  WHERE jobKey = "+str(jobID)
        c.execute(sqlComm1)

        conn.commit()
        c.close()

        return redirect("../adminJobDashboard.html")

#helper function
def shortenString(strInput):
    if len(strInput) > 150:
        return strInput[0:151]+"..."
    else:
        return strInput

# A decorator used to tell the application which URL is associated function
@adminPages.route('/adminUsers.html', methods =['GET', 'POST'])
def adminUsersFUNC():
    if request.method == 'POST' and request.form.get("logout")!=None:
        session.pop("userID", None)
        session.pop("email", None)
        session.pop("password", None)
        session.pop("userType", None)
        return render_template('home.html', boolean=True) 
    elif session["userID"] != 5:
        #send the user back to login page if they are not the admin user
        return redirect("../loginHTML.html")
    elif request.method == 'GET':
        #connection to the database module
        conn = sqlite3.connect("data.db")
        # allow for SQL commands to be run
        c = conn.cursor()
        
        sqlComm1 = "SELECT * FROM LoginInfo"
        row = c.execute(sqlComm1).fetchall()
        print(row)

        userID = []
        userEmail = []
        userPassword = []
        userType = []

        loopCounter = 0
        for profiles in row:
            print(profiles)
            innerCounter = 0
            for attributes in profiles:
                print(attributes)
                if innerCounter == 0:
                    userID.append(attributes)
                elif innerCounter == 1:
                    userEmail.append(attributes)
                elif innerCounter == 2:
                    userPassword.append(attributes)
                elif innerCounter == 3:
                    userType.append(attributes)
                innerCounter += 1
            loopCounter += 1

        conn.commit()
        c.close()
        return render_template('adminUsers.html', counter = loopCounter, userID = userID, userEmail = userEmail, userPassword = userPassword, userType = userType)
    elif request.method == 'POST':
        if (request.form.get("deleteUserID") != None):
            deleteUser = request.form.get("deleteUserID")
            print(deleteUser)

            #connection to the database module
            conn = sqlite3.connect("data.db")
            # allow for SQL commands to be run
            c = conn.cursor()
            
            sqlComm1 = "DELETE FROM LoginInfo WHERE userKey = "+deleteUser
            row = c.execute(sqlComm1).fetchall()

            conn.commit()
            c.close()
            return redirect('../adminUsers.html')
        elif (request.form.get("editUserID")!= None):
            session['editUserID'] = request.form.get("editUserID")
            return redirect("../editUserAdmin.html")
        elif (request.form.get("addUser") != None):
            return redirect("../addUserAdmin.html")

@adminPages.route('/editUserAdmin.html', methods =['GET', 'POST'])
def adminEditUserFUNC():
    if request.method == 'POST' and request.form.get("logout")!=None:
        session.pop("userID", None)
        session.pop("email", None)
        session.pop("password", None)
        session.pop("userType", None)
        return render_template('home.html', boolean=True) 
    elif request.method == 'GET':
            editUserID = session["editUserID"]
            #connection to the database module
            conn = sqlite3.connect("data.db")
            # allow for SQL commands to be run
            c = conn.cursor()
                
            sqlComm1 = "SELECT * FROM LoginInfo WHERE userKey = "+editUserID
            row = c.execute(sqlComm1).fetchall()

            editUser = []
            for x in row[0]:
                print("looping")
                editUser.append(x)
            print(editUser)

            conn.commit()
            c.close()
            return render_template('editUserAdmin.html', editUser = editUser)
    elif request.method == 'POST': 
            editUser = session['editUserID']
            print(editUser)
            email = request.form.get("email")
            print(email)
            
            password = request.form.get("password")
            print(password)

            #connection to the database module
            conn = sqlite3.connect("data.db")
            # allow for SQL commands to be run
            c = conn.cursor()
                
            sqlComm1 = "UPDATE LoginInfo SET email = '"+str(email)+"', password = '"+str(password)+"' WHERE userKey = "+editUser
            c.execute(sqlComm1)

            conn.commit()
            c.close()
            return redirect("../adminUsers.html")
        
@adminPages.route('/addUserAdmin.html', methods =['GET', 'POST'])
def adminAddUserFUNC():
    if request.method == 'POST' and request.form.get("logout")!=None:
        session.pop("userID", None)
        session.pop("email", None)
        session.pop("password", None)
        session.pop("userType", None)
        return render_template('home.html', boolean=True) 
    elif request.method == 'GET':
        return render_template('addUserAdmin.html')
    elif request.method == 'POST':
        #connection to the database module
        conn = sqlite3.connect("data.db")
        # allow for SQL commands to be run
        c = conn.cursor()
                
        #sqlComm1 = "SELECT LAST (userKey) FROM LoginInfo"
        sqlComm1 = "SELECT userKey FROM LoginInfo ORDER BY userKey DESC LIMIT 1"
        lastID = c.execute(sqlComm1).fetchone()
        print("THIS IS THE LAST ID IN THE TABLE "+str(lastID[0]))

        userKey = int(lastID[0]) + 1
        email = request.form.get("email")
        password = request.form.get("password")
        userType = request.form.get("userType")
        
        sqlComm2 = "INSERT INTO LoginInfo (userKey, email, password, userType) VALUES('"+str(userKey)+"', '"+str(email)+"', '"+str(password)+"', '"+str(userType)+"')"
        
        c.execute(sqlComm2)
        conn.commit()
        c.close()
        return redirect("../adminUsers.html")
