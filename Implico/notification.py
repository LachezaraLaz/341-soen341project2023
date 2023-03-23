import sqlite3
from flask import Flask, request, render_template, Blueprint, redirect, session

#initializing Blueprint
notification = Blueprint('notification', __name__)

@notification.route("/notification.html", methods = ['GET', 'POST'])
def notif():
    id = session.get('userID')
    ll = session.get('email')
    print(id)
    print (ll)
    if (session.get('userID') == None):
        return redirect('../loginHTML.html')
    else:
        # notifKey = 1
        # if (session.get('userType') == 'student'):
        #     message = "mon calisse"
        #     conn = sqlite3.connect("data.db")
        #     c = conn.cursor()
        #     newNotif = "INSERT INTO Notifications (notifKey, userID, message) VALUES (" + str(notifKey) + "," + str(id) + "," + str(message) + ")"
        #     c.execute(newNotif)
        #     conn.commit()
        #     c.close()
            return render_template('notification.html')
    
@notification.route("/JobDescription.html", methods = ['GET', 'POST'])
def JobDescription():
    if request.method == 'GET':
        return render_template('JobDescription.html')
    elif (request.method == 'POST' ):
        applyButton = request.form['applyButton']
        print(applyButton)
        if (session.get('userType') == 'student'):
            conn = sqlite3.connect("data.db")
            c = conn.cursor()
            date = c.execute("SELECT date('now')").fetchone()
            intoSTR = ''.join(map(str, date)).replace("-", "/")
            print(intoSTR)
            notifIfNone = c.execute("SELECT notifKey FROM Notifications").fetchone()
            if (notifIfNone == None):
                c.execute("INSERT INTO Notifications VALUES ("+str(1)+","+str(session.get('userID'))+", 'A candidate has applied to one of your jobs!' ,'" + str(intoSTR) + "')")
                conn.commit()
                c.close()
                return redirect('notification.html')
            else:
                notifKey = c.execute("SELECT notifKey FROM Notifications ORDER BY notifKey DESC LIMIT 1").fetchone()
                intoINT = int(''.join(map(str, notifKey)))
                c.execute("INSERT INTO Notifications VALUES ("+str(intoINT+1)+","+str(session.get('userID'))+", 'A candidate has applied to one of your jobs!' ,'" + str(intoSTR) + "')")
                conn.commit()
                c.close()
                return redirect('notification.html')
    
