#import flask into the file
from flask import Flask, flash, Blueprint, render_template, request, session, redirect, url_for
#stuff for file uploading
import os
from werkzeug.utils import secure_filename
#import python database sqlite3 (based in sql)
import numpy as np

import sqlite3

UPLOAD_FOLDER = '../uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'docx', 'jpg', 'jpeg', 'html'}

userProfile = Blueprint('userprofile', __name__)

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
 


#CODE FOR EDIT PROFILE PAGE
@userProfile.route("/editProfile.html", methods=['GET', 'POST'])
def editProfile():
    #storing the profile key in a variable
    profileKey = session["profileID"]

    #WHEN THE USER SUBMITS THE 
    if request.method == 'POST':
        #CONNECTION TO DATABASE
        # connection to the database module
        conn = sqlite3.connect("data.db")
        # allow for SQL commands to be run
        c = conn.cursor()

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
        updateEntry = "UPDATE UserProfiles SET firstName='"+str(firstName)+"', lastName='"+str(lastName)+"', bio='"+str(bio)+"', educInstitution='"+str(school)+"', educDegree='"+str(program)+"', location='"+str(location)+"', contactInfo='"+str(contact)+"', portfolioLink='"+str(portfolio)+"' WHERE profileKey="+str(profileKey)
        c.execute(updateEntry)

        #------------------

        #STEP 2 - COLLECT, VERIFY AND UPDATE USER'S WORK EXPERIENCES
        #fetch inputs for work experiences from form - each is returning a list
        experienceIDs = request.form.getlist('expID')
        print(experienceIDs)
        jobTitles = request.form.getlist('JobTitle')
        employers = request.form.getlist('Employer')
        startDates = request.form.getlist('StartDate')
        endDates = request.form.getlist('endDate')
        descriptions = request.form.getlist('Description')
        skills = request.form.getlist('Skills')

        #fetch all work experience IDs tied to the user's profile
        fetchExpIDs = "SELECT expKey FROM WorkExperience WHERE profileID="+str(profileKey)+" ORDER BY expKey ASC"
        databaseIDs = c.execute(fetchExpIDs).fetchall()
        databaseExpIDs = []
        count = 0
        for i in databaseIDs:
            databaseExpIDs.append(databaseIDs[count][0])
            count+=1
        print(databaseExpIDs)

        #loop through to verify if a position was deleted by the user
        for databaseID in databaseExpIDs:
            #if the experience was deleted by user
            if str(databaseID) not in experienceIDs:
                print(databaseID in experienceIDs)
                deleteID = "DELETE FROM WorkExperience WHERE expKey="+str(databaseID)
                print(databaseID)
                c.execute(deleteID)

        #fetch the last work experience key in database
        lastExpKey = int(c.execute("SELECT expKey FROM WorkExperience ORDER BY expKey DESC").fetchall()[0][0])
        print(lastExpKey)

        #loop through to verify if a position has been added or edited
        for work in experienceIDs:
            #if a work experince has been added
            if "new" in work:
                #incremeent the key to get a new experience key
                lastExpKey+=1
                newKey = lastExpKey
                
                #getting all the values from the form for this entry
                position = jobTitles[0]
                print(position)
                employer = employers[0]
                startDate = startDates[0].split("/")
                startMonth = startDate[0]
                startYear = startDate[1]
                endDate = endDates[0].split("/")
                endMonth = endDate[0]
                endYear = endDate[1]
                desc = descriptions[0]
                skill = skills[0]

                #remove these values from the form lists
                jobTitles.pop(0)
                employers.pop(0)
                startDates.pop(0)
                endDates.pop(0)
                descriptions.pop(0)
                skills.pop(0)

                #inserting this data into the database
                insertWork = "INSERT INTO WorkExperience (expKey, profileID, position, employer, startMonth, startYEAR, endMonth, endYear, expDescription, skills) VALUES ("+str(newKey)+", "+str(profileKey)+", '"+str(position)+"', '"+str(employer)+"', "+str(startMonth)+", "+str(startYear)+", "+str(endMonth)+", "+str(endYear)+", '"+str(desc)+"', '"+str(skill)+"')"
                c.execute(insertWork)
            
            #when user was updating a work experience
            else:
                #getting all the values from the form for this entry
                position = jobTitles[0]
                employer = employers[0]
                startDate = startDates[0].split("/")
                startMonth = startDate[0]
                startYear = startDate[1]
                endDate = endDates[0].split("/")
                endMonth = endDate[0]
                endYear = endDate[1]
                desc = descriptions[0]
                skill = skills[0]

                #remove these values from the form lists
                jobTitles.pop(0)
                employers.pop(0)
                startDates.pop(0)
                endDates.pop(0)
                descriptions.pop(0)
                skills.pop(0)

                #updating the entry into the database
                updateWork = "UPDATE WorkExperience SET position='"+str(position)+"', employer='"+str(employer)+"', startMonth="+str(startMonth)+", startYEAR="+str(startYear)+", endMonth="+str(endMonth)+", endYear="+str(endYear)+", expDescription='"+str(desc)+"', skills='"+str(skill)+"' WHERE profileID="+str(profileKey)+" AND expKey="+str(work)
                c.execute(updateWork)
        
        #commit changes before proceeding with process a file
        conn.commit()
        c.close()


        #------------------

        #STEP 3 - PROCESS FILE UPLOAD
        
        #store the uploaded file
        resume = request.files['resume']
        print(resume.filename)
        
        #if user uploads an acceptable file
        if resume and allowed_file(resume.filename):
            #CONNECTION TO DATABASE
            # connection to the database module
            conn = sqlite3.connect("data.db")
            # allow for SQL commands to be run
            c = conn.cursor()
            filename = secure_filename(resume.filename)
            print("after secure_filename")

            #save file into upload file
            resume.save(os.path.join("Implico/uploads", filename))
            #save the filename to the database
            fileToDatabase = "UPDATE UserProfiles SET resumeFilename='../uploads/"+str(resume.filename)+"' WHERE profileKey="+str(profileKey)
            c.execute(fileToDatabase)
            conn.commit()
            c.close() 
            #after edits have been stored in database, redirect to user's profile page
            return redirect("../profileTempHTML.html")
        #if the user did not select a file
        elif resume.filename == '':
            print("no file selected")
            flash("no file selected")
            return redirect("../profileTempHTML.html")
        elif 'file' not in request.files:
            print("no file")
            return redirect("../profileTempHTML.html")
    

    #WHEN THE USER LOADS THE PAGE
    elif request.method == 'GET':
        #CONNECTION TO DATABASE
        # connection to the database module
        conn = sqlite3.connect("data.db")
        # allow for SQL commands to be run
        c = conn.cursor()
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
        res = str(userProfile[10])
        print(fname+", "+lname+", "+bio+", "+sc+", "+pro+", "+loc+", "+con+", "+port)

        c.close()

       #RENDER THE TEMPLATE WITH DATA FROM THE DATABASE
        return render_template('editProfile.html', firstName=fname, lastName=lname, userBio=bio, location=loc, contact=con, portfolio=port, school=sc, program=pro, resume=res, workExperience=workExps)

#fchecks if 
def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
#steps for profile page:
#1 - read session variables
#2 - use session variable values to search the database for the use profile and the job experience
#3 - fetch data about profile and jobs from database
#4 -