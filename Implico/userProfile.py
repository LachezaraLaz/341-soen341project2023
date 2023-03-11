#import flask into the file
from flask import Flask, flash, Blueprint, render_template, request, session, redirect, url_for
#stuff for file uploading
import os
from werkzeug.utils import secure_filename
#import python database sqlite3 (based in sql)
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
        updateEntry = "UPDATE UserProfiles SET firstName='"+str(firstName)+"', lastName='"+str(lastName)+"', bio='"+str(bio)+"', educInstitution='"+str(school)+"', educDegree='"+str(program)+"', location='"+str(location)+"', contactInfo='"+str(contact)+"', portfolioLink='"+str(portfolio)+"' WHERE profileKey="+str(profileKey)
        c.execute(updateEntry)

        #------------------

        #STEP 2 - COLLECT, VERIFY AND UPDATE USER'S WORK EXPERIENCES
        #fetch inputs for work experiences from form - each is returning a list
        expIDs = request.form.getlist('expID')
        jobTitles = request.form.getlist('JobTitle')
        employers = request.form.getlist('Employer')
        startDates = request.form.getlist('StartDate')
        endDates = request.form.getlist('endDate')
        descriptions = request.form.getlist('Description')
        skills = request.form.getlist('Skills')

        #fetch all work experience IDs tied to the user's profile
        fetchExpIDs = "SELECT expKey FROM WorkExperience WHERE profileID="+str(profileKey)+" ORDER BY expKey ASC"
        databaseExpIDs = c.execute(fetchExpIDs).fetchall()

        #loop through to verify if a position was deleted by the user
        for databaseExpID in databaseExpIDs:
            #if the experience was deleted by user
            if databaseExpID[0] not in expIDs:
                deleteID = "DELETE FROM WorkExperience WHERE expKey="+str(databaseExpID[0])
                print(databaseExpID[0])
                c.execute(deleteID)
                databaseExpIDs.remove(databaseExpID)

        #fetch the last work experience key in database
        lastExpKey = c.execute("SELECT expKey FROM WorkExperience ORDER BY expKey DESC").fetchall()[0]

        #loop through to verify if a position has been added or edited
        for work in expIDs:
            #if a work experince has been added
            if "new" in work:
                #incremeent the key to get a new experience key
                lastExpKey+=1
                newKey = lastExpKey
                
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

                #inserting this data into the database
                insertWork = "INSERT INTO WorkExperience (expKey, profileID, position, employer, startMonth, startYEAR, endMonth, endYear, expDescription, skills) "
                insertValues = "("+int(newKey)+", "+int(profileKey)+", '"+str(position)+"', '"+str(employer)+"', "+int(startMonth)+", "+int(startYear)+", "+int(endMonth)+", "+int(endYear)+", '"+str(desc)+"', '"+str(skill)+"')"
                insertIntoDatabase = insertWork+insertValues
                c.execute(insertIntoDatabase)
            
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

        #CONNECTION TO DATABASE
        # connection to the database module
        conn = sqlite3.connect("data.db")
        # allow for SQL commands to be run
        c = conn.cursor()

        #check if the post request received a file
        if 'file' not in request.files:
            flash("no file part")
            return redirect(request.url)
        
        #store the uploaded file
        resume = request.files['resume']

        #if the user did not select a file
        if resume.filename == '':
            flash("no file selected")
            return redirect(request.url)
        
        #check 
        
        #if user uploads an acceptable file
        if resume and allowed_file(resume.filename):
            filename = secure_filename(resume.filename)
            #save file into upload file
            resume.save("../uploads", filename)
            #save the filename to the database
            fileToDatabase = "UPDATE UserProfiles SET resumeFilename='../uploads/"+str(resume.filename)+"' WHERE profileKey="+str(profileKey)
            c.execute(fileToDatabase)
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