import sqlite3
from flask import Flask, request, render_template, Blueprint, redirect, session
from .signup import logout
#initializing Blueprint
feedback = Blueprint('feedback', __name__)

@feedback.route('/submitFeedback.html',methods = ['POST','GET'])
def giveFeedback():
    if request.method == 'POST' and request.form.get("logout")!=None:
        logout()
        return redirect('home.html', boolean=True)
    elif request.method == 'GET':
        if(session.get("userType") == None):
            return redirect("/loginHTML.html")
        elif (session.get("userType") == "student"):
            return render_template("candidateSubmitFeedback.html")
        else:
            return render_template("employerSubmitFeedback.html")
        
    else:
        # POST method
        conn = sqlite3.connect("data.db")
        c = conn.cursor()
        feedbackMessage = request.form['feedback']
        userID = session.get("userID")
        email = session.get("email")
        lastKey = c.execute("SELECT feedbackKey FROM userFeedback ORDER BY feedbackKey DESC LIMIT 1").fetchone()[0]
        insertEntry = "INSERT INTO userFeedback VALUES(" + str(lastKey+1) + ",'" + feedbackMessage +"'," + str(userID) + ",'" + email +"')"
        c.execute(insertEntry)
        conn.commit()
        c.close()
        if(session.get("userType") == "student"):
            return redirect("/indexCandidate.html")
        else:
            return redirect("/indexEmployer.html")

    

@feedback.route('/adminViewFeedback.html', methods = ['POST','GET'])
def adminFeedback():
    if request.method == 'POST' and request.form.get("logout")!=None:
        logout()
        return redirect('home.html')
    elif request.method == 'GET':
        # not logged in or not admin
        if(session.get("userType") == None or session.get("userType") != "admin"):
            return redirect('/loginHTML.html')
        else:
            # connection to the database module
            conn = sqlite3.connect("data.db")
            c = conn.cursor()
            feedbackEntries = c.execute("SELECT * FROM userFeedback").fetchall()
            return render_template("adminViewFeedback.html", feedbackEntries = feedbackEntries) 
