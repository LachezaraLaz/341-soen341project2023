#importing the sqlite3 module to handle database
import sqlite3
import datetime
#importing Flask and other modules
from flask import Flask, request, render_template, redirect, session, Blueprint
#initializing blueprint
employerDashboard = Blueprint('employerDashboard', __name__)

def notifMessage(messageCode, jobPostingID):
    # messageCode Legend:
    # 1 -> Selected for Interview
    # 2 -> Rejected for Interview
    if messageCode == 1:
        return "You have been selected for an interview for a job! (jobPostingID = " + jobPostingID + "). Congratulations!"
    else:
        return "You have unfortunately been rejected for an interview for a job (jobPostingID = " + jobPostingID + "). Better luck next time lol."

@employerDashboard.route('/jobDashboardHTML.html', methods = ['GET','POST'])
def jobDashboard():
    if request.method == 'POST' and request.form.get("logout")!=None:
        session.pop("userID", None)
        session.pop("email", None)
        session.pop("password", None)
        session.pop("userType", None)
        return render_template('home.html', boolean=True) 
    elif request.method == 'GET':
        if(session.get("userID") == None or session.get("userType") == "student" or session.get("userType") == "admin"):
            # not logged in or is wrong user type
            if(session.get("userID") == None):
                return redirect("/loginHTML.html")
            elif session.get("userType") == "student":
                return redirect("/VUJP")
            else:
                return redirect("/adminJobDashboard.html")
        else:
            # connection to the database module
            conn = sqlite3.connect("data.db")
            c = conn.cursor()
            jobPostings = c.execute("SELECT * FROM JobPostings WHERE userID=" + str(session["userID"]) + "" ).fetchall()
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
            session["addPostingID"] = 1
            return redirect("/editJobPosting.html")
        # edit button functionality
        elif(request.form.get("editPostingID") != None):
            session["editPostingID"] = request.form["editPostingID"]
            print("session id is", session["editPostingID"])
            return redirect("/editJobPosting.html")

@employerDashboard.route("/editJobPosting.html",methods = ['GET','POST'])
def editPosting():
    if request.method == 'POST' and request.form.get("logout")!=None:
        session.pop("userID", None)
        session.pop("email", None)
        session.pop("password", None)
        session.pop("userType", None)
        return render_template('home.html', boolean=True) 
    elif request.method == 'GET':
        if(session.get("userID") == None or session.get("userType") == "student" or session.get("userType") == "admin"):
            # not logged in or wrong user type
            #if(session.get("userID") == None):
                #return redirect("/loginHTML.html")
            if session.get("userType") == "student":
                return redirect("/VUJP")
            else:
                return redirect("/adminJobDashboard.html")
        else:
            # logged in and correct user type
            if(session.get("editPostingID") != None):
                # all good to load (logged in and editposting id set)
                conn = sqlite3.connect("data.db")
                c = conn.cursor()
                jobPosting = c.execute("SELECT * FROM JobPostings WHERE jobKey=" + session["editPostingID"]).fetchone()
                print(jobPosting)
                pageTitle = "Edit Job Posting"
                return render_template("/editJobEmployer.html", title = jobPosting[2], company = jobPosting[3], description = jobPosting[4], requirements = jobPosting[5], location = jobPosting[6], salary = jobPosting[7], pageTitle = pageTitle)
            elif session.get("addPostingID") != None:
                # add posting id set and logged in as employer -> new posting entry
                pageTitle = "New Job Posting"
                return render_template("/editJobEmployer.html", pageTitle = pageTitle)
            else:
                # not add or edit
                return redirect("/jobDashboardHTML.html")
    elif request.method == 'POST':
        conn = sqlite3.connect("data.db")
        c = conn.cursor()
        if(session.get("editPostingID") != None):
            # update existing table record
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
        elif (session.get("userID") != None):
            # New table record
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
            session.pop("addPostingID", None)
            return redirect("/jobDashboardHTML.html")
@employerDashboard.route("/jobApplicantsEmployer.html", methods = ['GET','POST'])
def jobApp():
    if request.method == 'POST' and request.form.get("logout")!=None:
        session.pop("userID", None)
        session.pop("email", None)
        session.pop("password", None)
        session.pop("userType", None)
        return render_template('home.html', boolean=True) 
    elif(request.method == 'GET'):
        if(session.get("userID") != None):
            # find all applicants of their jobs then make table
            conn = sqlite3.connect("data.db")
            c = conn.cursor()
            print("user ID is ",session["userID"])
            appQuery = "SELECT * FROM JobApplicants WHERE employerID='" + str(session["userID"]) + "'" 
            jobApplicants = c.execute(appQuery).fetchall()
            print(jobApplicants)
            return render_template("/jobApplicantsEmployer.html", jobApplicants = jobApplicants)
        else:
            return render_template("/jobApplicantsEmployer.html")
    elif request.method == 'POST':
        print("post lol")
        conn = sqlite3.connect("data.db")
        c = conn.cursor()
        print(request.form)
        
        if 'View Candidate Profile' in request.form:
            applicant = request.form['jobApplicantID']
            profileApplicant = c.execute("SELECT * FROM UserProfiles WHERE profileKey="+str(applicant)).fetchone()

            #find work experience records user profileKey in the WorkExperience table
            fetchWork = c.execute("SELECT * FROM WorkExperience WHERE profileID="+str(applicant)).fetchall()
    
            #FORMATING DATA TO BE INSERTED ONTO HTML PAGE
            #separating fields of the record
            name = str(profileApplicant[2])+" "+str(profileApplicant[3])
            bio = str(profileApplicant[4])
            educ = str(profileApplicant[5])+" - "+str(profileApplicant[6])
            loc = str(profileApplicant[7])
            con = str(profileApplicant[8])
            port = "\""+str(profileApplicant[9])+"\""

            conn.commit()
            c.close()
    
            #RENDER THE TEMPLATE WITH DATA FROM THE DATABASE
            return render_template('profileTempHTML.html', fullName=name, userBio=bio, education=educ, location=loc, contact=con, portfolio=port, workExperience=fetchWork)
 
        if 'Choose For Interview' in request.form:
            print("in 1")
            # create notification for user and update selected candidate field
            userIDTo = request.form["jobApplicantID"]
            postingID = request.form["jobPostingID"]
            timeNow = datetime.datetime.now()
            timeNowFormatted = timeNow.strftime("%Y-%m-%d-%X")
            lastNotif = c.execute("SELECT notifKey FROM Notifications ORDER BY notifKey DESC").fetchone()[0]
            print("last notif is ", lastNotif)
            newNotif = "INSERT INTO Notifications VALUES(" + str(lastNotif+1) + "," + str(session["userID"]) + "," + str(userIDTo) + ",'" + notifMessage(1,postingID) + "','" + str(timeNowFormatted) + "')"
            print("newNotif is ", newNotif)
            changeCandidate = "UPDATE JobPostings SET selectedCandidate = " + str(userIDTo) + " WHERE jobKey= " + str(postingID)
            c.execute(changeCandidate)
            c.execute(newNotif)
            conn.commit()
            c.close()
            return redirect("/jobApplicantsEmployer.html")
        elif 'Reject Candidate' in request.form:
            print("in 2")
            userIDTo = request.form["jobApplicantID"]
            postingID = request.form["jobPostingID"]
            timeNow = datetime.datetime.now()
            timeNowFormatted = timeNow.strftime("%Y-%m-%d-%X")
            lastNotif = c.execute("SELECT notifKey FROM Notifications ORDER BY notifKey DESC LIMIT 1").fetchone()[0]
            newNotif = "INSERT INTO Notifications VALUES(" + str(lastNotif + 1) + "," + str(session["userID"]) + "," + str(userIDTo) + ",'" + notifMessage(2,postingID) + "','" + str(timeNowFormatted) + "')"
            print("newNotif is ", newNotif)
            c.execute(newNotif)
            conn.commit()
            c.close()
            return redirect("/jobApplicantsEmployer.html")
            
        
@employerDashboard.route("/DB")
def applDummys():
        conn = sqlite3.connect("data.db")
        c = conn.cursor()
        query2 = "INSERT INTO Notifications VALUES (1,10, 1,'Welcome To Implico', '3/25/2023')"
        c.execute(query2)
        conn.commit()
        c.close()
        return "added"
