import sqlite3
from flask import Flask, request, render_template, Blueprint, redirect, session

#initializing Blueprint
notification = Blueprint('notification', __name__)

@notification.route("/notification.html", methods = ['GET', 'POST'])
def notif():
    #if no user has logged in yet, then they are redirected to login page to login.
    if (session.get('userID') == None):
        return redirect('../loginHTML.html')
    else:
        return render_template('notification.html')
    
@notification.route("/JobDescription.html", methods = ['GET', 'POST'])
def JobDescription():
    if (request.method == 'GET'):
        # connection to the database module
        conn = sqlite3.connect("data.db")
        c = conn.cursor()
        whichJob = session['jobKey']
        jobPostings = c.execute("SELECT * FROM JobPostings WHERE jobKey = " + str(whichJob)).fetchall()
        # print(c.execute("SELECT * FROM JobPostings WHERE jobKey = "+str(whichJob)).fetchall())
        return render_template("/JobDescription.html", jobPosting = jobPostings)

     
    #from the form for the apply button in the JobDescription file 
    if (request.method == 'POST' ):
        applyButton = request.form['applyButton']
        print(applyButton)
        #this only happens when the user is a student, will have another when we do employer
        if (session.get('userType') == 'student'):
            conn = sqlite3.connect("data.db")
            c = conn.cursor()
            #fetching todays date
            date = c.execute("SELECT date('now')").fetchone()
            #replacing them with / because the system understood - as minus
            intoSTR = ''.join(map(str, date)).replace("-", "/")
            notifIfNone = c.execute("SELECT notifKey FROM Notifications").fetchone()
            #if no notifications have been added to the database so far
            if (notifIfNone == None):
                c.execute("INSERT INTO Notifications VALUES ("+str(1)+","+str(session.get('userID'))+", 'A candidate has applied to one of your jobs!' ,'" + str(intoSTR) + "')")
                conn.commit()
                c.close()
                return redirect('/notification.html')
            #if it is not the first notification in the database
            else:
                notifKey = c.execute("SELECT notifKey FROM Notifications ORDER BY notifKey DESC LIMIT 1").fetchone()
                intoINT = int(''.join(map(str, notifKey)))
                c.execute("INSERT INTO Notifications VALUES ("+str(intoINT+1)+","+str(session.get('userID'))+", 'A candidate has applied to one of your jobs!' ,'" + str(intoSTR) + "')")
                #selecting necessary notifications
                newNotif = c.execute("SELECT * FROM Notifications WHERE userID ="+str(session.get('userID'))).fetchall()
                conn.commit()
                c.close()
                return render_template('/notification.html', message = str(newNotif[1]))
    
