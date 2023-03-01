#import flask, render template, and request into the file
from flask import Flask, render_template, request, session, redirect, url_for
#import python database sqlite3 (based in sql)
import sqlite3


#create flask object
app = Flask(__name__)

#session data gets encrypted by this secret key 
app.secret_key = "inasisamazing"

#CODE FOR THE USER PROFILE PAGE
#temporary file path
@app.route("/profileHTML.html", methods=['GET', 'POST'])
#home page
def profile():
    #CONNECTION TO DATABASE
    # connection to the database module
    conn = sqlite3.connect("data.db")
    # allow for SQL commands to be run
    c = conn.cursor()

    #SHOULDN'T HAPPEN
    if request.method == 'POST':
        print("your mom caca lala")
    
    #WHEN THE PAGE GETS LOADED
    else:
        #STORING THE SESSION VAR OF THE USER'S ID IN A VAR
        userID = session["userID"]

        #RETRIEVING DATA FROM THE TABLES IN THE DATABASE
        #find profile record using userID in the userProfile table
        sqlComm1 = "SELECT * FROM UserProfiles WHERE userID="+str(userID)
        userProfile = c.execute(sqlComm1).fetchone()
        #storing profileKey in a variable
        profileKey = userProfile[0]
        #find work experience records user profileKey in the WorkExperience table
        sqlComm2 = "SELECT * FROM WorkExperience WHERE profileID="+str(profileKey) 
        workExps = c.execute(sqlComm2).fetchall()

        #

        print(userProfile)

    return render_template('loginHTML.html', boolean=True)


#CODE FOR EDIT PROFILE PAGE
@app.route("/signUpHTML.html", methods=['GET', 'POST'])
def editProfile():
    if request.method == 'POST':
        #after edits have been stored in database, redirect to user's profile page
        return redirect(url_for("/loginHTML.html"))
    else:
        return

#running flask app
if __name__ == "__main__":
    app.run(debug=True)

#steps for profile page:
#1 - read session variables
#2 - use session variable values to search the database for the use profile and the job experience
#3 - fetch data about profile and jobs from database
#4 - 
