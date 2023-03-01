#import flask into the file
from flask import Flask, Blueprint, render_template, request, session, redirect, url_for
#import python database sqlite3 (based in sql)
import sqlite3

userProfile = Blueprint('userprofile', __name__)


#CODE FOR THE USER PROFILE PAGE
@userProfile.route('/profileTempHTML.html', methods=['GET', 'POST'])
#user profile page
def profile():
    #CONNECTION TO DATABASE
    # connection to the database module
    conn = sqlite3.connect("data.db")
    # allow for SQL commands to be run
    c = conn.cursor()

    #SHOULDN'T HAPPEN
    if request.method == 'POST':
        print("your mom caca lala")
        return
    
    #WHEN THE PAGE GETS LOADED
    else:
        #STORING THE SESSION VAR OF THE USER'S ID IN A VAR
        userID = 1 #session["userID"]

        #RETRIEVING DATA FROM THE TABLES IN THE DATABASE
        #find profile record using userID in the userProfile table
        fetchProfile = "SELECT * FROM UserProfiles WHERE userID="+str(userID)
        userProfile = c.execute(fetchProfile).fetchone()
        #storing profileKey in a variable
        profileKey = userProfile[0]
        #find work experience records user profileKey in the WorkExperience table
        fetchWork = "SELECT * FROM WorkExperience WHERE profileID="+str(profileKey) 
        workExps = c.execute(fetchWork).fetchall()


        #FORMATING DATA TO BE INSERTED ONTO HTML PAGE
        #separating fields of the record
        name = str(userProfile[2])+" "+str(userProfile[3])
        bio = str(userProfile[4])
        educ = str(userProfile[5])+" - "+str(userProfile[6])
        loc = str(userProfile[7])
        con = str(userProfile[8])
        port = "\""+str(userProfile[9])+"\""
        #creating string holding rows for work experience table
        workExpTable = expTableCreator(workExps)

        #RENDER THE TEMPLATE WITH DATA FROM THE DATABASE
        return render_template('loginHTML.html', fullName=name, userBio=bio, education=educ, location=loc, contact=con, portfolio=port, workExperience=workExpTable)
    
#-----------
# function to create the work experience html table in profile function
def expTableCreator(records):
    rows = None # will contain all table rows at the end
    for record in records:
        # separating the content from each field of the record
        pos = str(record[2]) #
        emp = str(record[3]) #
        sDate = formatDate(record[4], record[5])
        eDate = formatDate(record[6], record[7])
        desc = str(record[8])
        ski = str(record[9])
        print(pos+" "+emp+" "+sDate+" "+eDate)
        # creating string containing table columns
        cols = "<td class=\"col-2\">"+pos+"</td>\n<td class=\"col-1\">"+emp+"</td>\n<td class=\"col-1\">"+sDate+"</td>\n<td class=\"col-1\">"+eDate+"</td>\n<td class=\"col-5\">"+desc+"</td>\n<td class=\"col-2\">"+ski+"</td>"

        # creating string containing table row with columns
        row = "<tr>"+cols+"</tr>"

        # concatinate row to rows
        rows = rows + row
    #return string containing all table rows
    return rows

#-----------
#function to format the date used in the expTable Creator
def formatDate(numM, numY):
    if int(numM) < 10:
        return "0"+str(numM)+"/"+str(numY)
    else:
        return str(numM)+"/"+str(numY)
     
        



#CODE FOR EDIT PROFILE PAGE
@userProfile.route("/signUpHTML.html", methods=['GET', 'POST'])
def editProfile():
    if request.method == 'POST':
        #after edits have been stored in database, redirect to user's profile page
        return redirect(url_for("/loginHTML.html"))
    else:
        return

#steps for profile page:
#1 - read session variables
#2 - use session variable values to search the database for the use profile and the job experience
#3 - fetch data about profile and jobs from database
#4 -