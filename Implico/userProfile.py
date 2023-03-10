#import flask into the file
from flask import Flask, flash, Blueprint, render_template, request, session, redirect, url_for
#from flask_sqlalchemy import SQLAlchemy
#import python database sqlite3 (based in sql)
import sqlite3

#stuff for file uploading
import os

UPLOAD_FOLDER = '../uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'docx', 'jpg', 'jpeg', 'html'}

userProfile = Blueprint('userprofile', __name__)


#userProfile.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
#userProfile.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#db = SQLAlchemy(userProfile)

#CODE FOR THE USER PROFILE PAGE
@userProfile.route('/profileTempHTML.html', methods=['GET', 'POST'])
#user profile page
def profile():

    #SHOULDN'T HAPPEN
    if request.method == 'POST':
        #CONNECTION TO DATABASE
        # connection to the database module
        conn = sqlite3.connect("data.db")
        # allow for SQL commands to be run
        c = conn.cursor()
        print("your mom caca lala")
        c.close()
        return
    
    #WHEN THE PAGE GETS LOADED
    elif request.method == 'GET':
        #CONNECTION TO DATABASE
        # connection to the database module
        conn = sqlite3.connect("data.db")
        # allow for SQL commands to be run
        c = conn.cursor()


        #STORING THE SESSION VAR OF THE USER'S ID IN A VAR
        userID = session["userID"]
        print(userID)


        #RETRIEVING DATA FROM THE TABLES IN THE DATABASE
        #find profile record using userID in the userProfile table
        fetchProfile = "SELECT * FROM UserProfiles WHERE userID="+str(userID)
        userProfile = c.execute(fetchProfile).fetchall()[0]
        #storing profileKey in a variable
        profileKey = str(userProfile[0])
        #find work experience records user profileKey in the WorkExperience table
        fetchWork = f"SELECT * FROM WorkExperience WHERE profileID={profileKey}"
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
        #workExpTable = expTableCreator(workExps)

        session["profileID"] = profileKey

        c.close()

        #RENDER THE TEMPLATE WITH DATA FROM THE DATABASE
        return render_template('profileTempHTML.html', fullName=name, userBio=bio, education=educ, location=loc, contact=con, portfolio=port, workExperience=workExps)
    
#-----------code not necessary------------------------
# function to create the work experience html table in profile function
def expTableCreator(records):
    rows = "" # will contain all table rows at the end
    for record in records:
        # separating the content from each field of the record
        pos = str(record[2]) 
        emp = str(record[3]) 
        sDate = formatDate(record[4], record[5])
        eDate = formatDate(record[6], record[7])
        desc = str(record[8])
        ski = str(record[9])
        print(pos+" "+emp+" "+sDate+" "+eDate)
        # creating string containing table columns
        cols = "<td class='col-2'>"+pos+"</td>\n<td class=\"col-1\">"+emp+"</td>\n<td class=\"col-1\">"+sDate+"</td>\n<td class=\"col-1\">"+eDate+"</td>\n<td class=\"col-5\">"+desc+"</td>\n<td class=\"col-2\">"+ski+"</td>"

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
@userProfile.route("/editProfile.html", methods=['GET', 'POST'])
def editProfile():
    #CONNECTION TO DATABASE
    # connection to the database module
    conn = sqlite3.connect("data.db")
    # allow for SQL commands to be run
    c = conn.cursor()

    #storing the profile key in a variable
    profileKey = session["profileID"]


    #WHEN THE USER SUBMITS THE 
    if request.method == 'POST':
        #STEP 1 - COLLECT AND UPDATE GENERAL PROFILE INFO
        #fetch general profile info from form
        firstName = request.form['FirstName']
        lastName = request.form['LastName']
        bio = request.form['Bio']
        location = request.form['Location']
        contact = request.form['ContactInfo']
        portfolio = request.form['PortfolioLink']
        school = request.form['Schoolname']
        program = request.form['Program']

        #update the database entry with the new user input
        updateEntry = "UPDATE UserProfiles SET firstName='"+firstName+"', lastName='"+lastName+"', bio='"+bio+"', educInstitution='"+school+"', educDegree='"+program+"', location='"+location+"', contactInfo='"+contact+"', portfolioLink='"+portfolio+"' WHERE profileKey="+str(profileKey)
        c.execute(updateEntry)

        #------------------

        #STEP 2 - COLLECT, VERIFY AND UPDATE USER'S WORK EXPERIENCES
        #fetch inputs for work experiences from form - each is returning a list
        expIDs = request.form.getlist['expID']
        jobTitles = request.form.getlist['JobTitle']
        employers = request.form.getlist['Employer']
        startDates = request.form.getlist['StartDate']
        endDates = request.form.getlist['endDate']
        descriptions = request.form.getlist['Description']
        skills = request.form.getlist['Skills']

        #fetch all work experience IDs tied to the user's profile
        fetchExpIDs = "SELECT expKey FROM WorkExperience WHERE profileID="+str(profileKey)

        #loop through to veri





        


        #check if a file was uploaded
        if 'file' not in request.files:
            flash('No file part')
            return redirect('../editProfile.html')
        #request the file
        file = request.files['resume']

        #save database manipulation into the database
        conn.commit()
        c.close()

        #after edits have been stored in database, redirect to user's profile page
        return redirect(url_for("../profileTempHTML.html"))
    

    #WHEN THE USER LOADS THE PAGE
    elif request.method == 'GET':
        #storing profile key
        profileID = session["profileID"]

        #FETCHING DATA
        fetchProfile = "SELECT * FROM UserProfiles WHERE profileKey="+str(profileID)
        userProfile = c.execute(fetchProfile).fetchone()
        #find work experience records user profileKey in the WorkExperience table
        fetchWork = "SELECT * FROM WorkExperience WHERE profileID="+str(profileID) 
        workExps = c.execute(fetchWork).fetchall()

        #FORMATTING THE DATA WE JUST FECTHED
        #separating fields of the record
        fname = str(userProfile[2])
        lname = str(userProfile[3])
        bio = str(userProfile[4])
        sc = str(userProfile[5])
        pro = str(userProfile[6])
        loc = str(userProfile[7])
        con = str(userProfile[8])
        port = str(userProfile[9])
        print(fname+", "+lname+", "+bio+", "+sc+", "+pro+", "+loc+", "+con+", "+port)

        c.close()

       #RENDER THE TEMPLATE WITH DATA FROM THE DATABASE
        return render_template('editProfile.html', firstName=fname, lastName=lname, userBio=bio, location=loc, contact=con, portfolio=port, school=sc, program=pro, workExperience=workExps)

#fchecks if 
def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
#steps for profile page:
#1 - read session variables
#2 - use session variable values to search the database for the use profile and the job experience
#3 - fetch data about profile and jobs from database
#4 -