import sqlite3
from flask import Flask, request, render_template, Blueprint, redirect, session

#initializing Blueprint
notification = Blueprint('notification', __name__)

@notification.route("/notification.html", methods = ['GET', 'POST'])
def notif():
    if request.method == 'POST' and request.form.get("logout")!=None:
        session.pop("userID", None)
        session.pop("email", None)
        session.pop("password", None)
        session.pop("userType", None)
        return render_template('home.html', boolean=True) 
    #if no user has logged in yet, then they are redirected to login page to login.
    elif (session.get('userID') == None):
        return redirect('../loginHTML.html')
    if (request.method == 'GET'):
        # connection to the database module
        conn = sqlite3.connect("data.db")
        c = conn.cursor()
        #selecting necessary notifications for the correct user
        newNotif = c.execute("SELECT * FROM Notifications WHERE userIDTo ="+str(session.get('userID'))).fetchall()
        userType = session["userType"]

        return render_template('/notification.html', newNotifs = newNotif, userType = userType)
    
    
@notification.route("/JobDescription.html", methods = ['GET', 'POST'])
def JobDescription():
    if request.method == 'POST' and request.form.get("logout")!=None:
        session.pop("userID", None)
        session.pop("email", None)
        session.pop("password", None)
        session.pop("userType", None)
        return render_template('home.html', boolean=True) 
    
    #displaying the correct job that was selected
    elif (request.method == 'GET'):
        # connection to the database module
        conn = sqlite3.connect("data.db")
        c = conn.cursor()
        # which job is selected and display the correct information
        whichJob = session['jobKey']
        jobPostings = c.execute("SELECT * FROM JobPostings WHERE jobKey = " + str(whichJob)).fetchall()
        # jobKey no longer needed
        session.pop("jobKey", None)
        return render_template("/JobDescription.html", jobPosting = jobPostings)

    #from the form for the apply button in the JobDescription file 
    if (request.method == 'POST' ):

        #this only happens when the user is a student, will have another when we do employer
        if (session.get('userType') == 'student'):
            #apply button
            applyButton = request.form['applyButton']
            print(applyButton)
            # connection to the database module
            conn = sqlite3.connect("data.db")
            c = conn.cursor()
            #fetching todays date
            date = c.execute("SELECT date('now')").fetchone()
            #replacing them with / because the system understood - as minus
            DateintoSTR = ''.join(map(str, date)).replace("-", "/")
            notifIfNone = c.execute("SELECT notifKey FROM Notifications").fetchone()

            #if no notifications have been added to the database so far
            if (notifIfNone == None):
                whichJob = request.form['viewJobs']

                # to who is the notification destined
                toWho = c.execute("SELECT userID FROM JobPostings WHERE jobKey ="+str(whichJob)).fetchone()
                tWintoINT = int(''.join(map(str, toWho)))
                
                #inserting all information needed
                c.execute("INSERT INTO Notifications VALUES ("+str(1)+","+str(session.get('userID'))+"," + str(tWintoINT) + ", 'A candidate has applied to one of your jobs!' ,'" + str(DateintoSTR) + "')")
                conn.commit()
                c.close()
                return redirect('/viewJobPosting.html')
    
            #if it is not the first notification in the database
            else:
                whichJob = request.form['viewJobs']

                #to know what notif key we are at
                notifKey = c.execute("SELECT notifKey FROM Notifications ORDER BY notifKey DESC LIMIT 1").fetchone()
                NotifIntoINT = int(''.join(map(str, notifKey)))
                
                #to know what jobApplicants key we are at
                appKey = c.execute("SELECT appKey FROM JobApplicants ORDER BY appKey DESC LIMIT 1").fetchone()
                AppIntoINT = int(''.join(map(str, appKey)))

                # to who is the notification destined
                toWho = c.execute("SELECT userID FROM JobPostings WHERE jobKey ="+str(whichJob)).fetchone()
                tWintoINT = int(''.join(map(str, toWho)))
                
                # getting user information, id and name
                fromWho = c.execute("SELECT profileKey FROM UserProfiles WHERE userID ="+str(session.get('userID'))).fetchone()
                fWintoINT = int(''.join(map(str, fromWho)))
                
                fromWhoFName = c.execute("SELECT firstName FROM UserProfiles WHERE userID ="+str(session.get('userID'))).fetchone()
                fromWhoLName = c.execute("SELECT lastName FROM UserProfiles WHERE userID ="+str(session.get('userID'))).fetchone()
                lastN = str(''.join(map(str, fromWhoFName)))
                firstN = str(''.join(map(str, fromWhoLName)))
                name = lastN+" "+firstN
            
                #inserting all information needed
                c.execute("INSERT INTO JobApplicants VALUES ("+str(AppIntoINT+1)+","+str(fWintoINT)+",'"+name+"',"+ str(tWintoINT) +","+ str(whichJob) +",'None')")
                c.execute("INSERT INTO Notifications VALUES ("+str(NotifIntoINT+1)+","+str(session.get('userID'))+"," + str(tWintoINT) + ", 'A candidate has applied to one of your jobs!' ,'" + str(DateintoSTR) + "')")
                conn.commit()
                c.close()
                return redirect('/viewJobPosting.html')
    
