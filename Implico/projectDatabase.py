# running this python file creates the database
# import the built-in database
import sqlite3
import re

# connection to the database module
conn = sqlite3.connect("data.db")

# allow for SQL commands to be run
c = conn.cursor()

# check if the database tables have been made
try:
    row = c.execute("SELECT userKey, email, password FROM LoginInfo").fetchall()
    lastKey = c.execute("SELECT userKey FROM LoginInfo ORDER BY userKey DESC").fetchone()[0]
    newRecord = "INSERT INTO LoginInfo VALUES ("+str(lastKey+1)+", 'test"+str(lastKey+1)+"@email.com', 'password"+str(lastKey+1)+"', 'employer')"
    row = c.execute(newRecord)
    delRecord = "DELETE FROM LoginInfo WHERE userKey="+str(lastKey+1)
    delRow = c.execute(delRecord)


except sqlite3.OperationalError:
    # first table: login user table
    c.execute("CREATE TABLE LoginInfo (userKey NUMBER, email TEXT, password TEXT, userType TEXT, PRIMARY KEY (userKey))")
    # second table: candidate user profile info table
    c.execute("CREATE TABLE UserProfiles (profileKey NUMBER, userID NUMBER, firstName TEXT, lastName TEXT, bio TEXT, educInstitution TEXT, educDegree TEXT, location TEXT, contactInfo TEXT, portfolioLink TEXT, resumeFilename TEXT, PRIMARY KEY (profileKey), FOREIGN KEY (userID) REFERENCES LoginInfo(userKey))")
    # third table: work experience table
    c.execute("CREATE TABLE WorkExperience (expKey NUMBER, profileID NUMBER, position TEXT, employer TEXT, startMonth NUMBER, startYEAR NUMBER, endMonth NUMBER, endYear NUMBER, expDescription TEXT, skills TEXT, PRIMARY KEY(expKey), FOREIGN KEY(profileID) REFERENCES UserProfiles(profileKey))")
    # fourth table: job postings table
    c.execute("CREATE TABLE JobPostings (jobKey NUMBER, userID NUMBER, title TEXT, company TEXT, jobDescription TEXT, requirements TEXT, workLocation TEXT, salary NUMBER, tags TEXT, creationDate TEXT, selectedCandidate TEXT, PRIMARY KEY(jobKey), FOREIGN KEY(userID) REFERENCES LoginInfo(userKey))")
    # fifth table: notification table
    c.execute("CREATE TABLE Notifications (notifKey NUMBER, userIDFrom NUMBER, userIDTo NUMBER, message TEXT, dateSent TEXT, PRIMARY KEY(notifKey), FOREIGN KEY(userIDFrom) REFERENCES LoginInfo(userKey), FOREIGN KEY(userIDTo) REFERENCES LoginInfo(userKey))")        
    # sixth table: job applicant table
    c.execute("CREATE TABLE JobApplicants (appKey NUMBER, profileID NUMBER,applicantName TEXT, employerID NUMBER, postingID NUMBER, appStatus TEXT, PRIMARY KEY(appKey), FOREIGN KEY(profileID) REFERENCES UserProfiles(profileKey), FOREIGN KEY(postingID) REFERENCES JobPostings(jobKey))")

    #seventh table: feedback
    c.execute("CREATE TABLE userFeedback (feedbackKey NUMBER, feedback TEXT,userID NUMBER, email TEXT, PRIMARY KEY(feedbackKey))")
    #insert into feedback table
    c.execute("INSERT INTO userFeedback VALUES (1, 'This is a sample feedback.',1, 'test1@email.com')")

    # inserting test data in LoginInfo
    c.execute("INSERT INTO LoginInfo VALUES (1, 'test1@email.com', '123pass', 'student')")
    c.execute("INSERT INTO LoginInfo VALUES (2, 'test3@email.com', '1234pass', 'employer')")
    c.execute("INSERT INTO LoginInfo VALUES (3, 'test2@email.com', '12345pass', 'student')")
    c.execute("INSERT INTO LoginInfo VALUES (4, 'test4@email.com', '123456pass', 'employer')")
    c.execute("INSERT INTO LoginInfo VALUES (5, 'admin@email.com', '1234567pass', 'admin')")

    # inserting test data in UserProfiles
    c.execute("INSERT INTO UserProfiles VALUES (1, 1, 'Jane', 'Doe', 'I am a second year Software Engineering student looking to further my career options', 'Concordia University', 'Software Engineering', 'Montreal', 'test1@email.com', 'github.com', '../file.pdf')")
    c.execute("INSERT INTO UserProfiles VALUES (2, 3, 'John', 'Doe', 'I am a third year Computer Science student and my code is out of this world', 'UQAM', 'Computer Science', 'Montreal', '111-222-3333', 'github.com/git_name', 'file2.pdf')")

    # inserting test data in WorkExperience
    c.execute("INSERT INTO WorkExperience VALUES (1, 1, 'Software Tester', 'AB Company', 1, 2022, 5, 2022, 'Executing testcases, discovering issues with the software and opening bugs accordingly', 'HTML, CSS, JS, C#')")
    c.execute("INSERT INTO WorkExperience VALUES (2, 1, 'Quality Assurance Intern', 'The Good COmpany', 4, 2019, 5, 2022, 'Debugging code of the flagship product', 'HTML, CSS, Node.js, React')")
    c.execute("INSERT INTO WorkExperience VALUES (3, 2, 'Software Developer Intern', 'Coding THE Code Inc', 1, 2022, 5, 2022, 'Contribute to the backend developement of the website as well as submitted pull requests to implement changes to code', 'C#, .NET Core, MongoDB')")
    c.execute("INSERT INTO WorkExperience VALUES (4, 2, 'Tools Intern', 'Software Inc', 4, 2019, 5, 2022, 'Develop an internal dashboard tool for students and provide reports on its performance on Salesforce', 'Salesforce, Python, Flask, PowerBI')")
    
    #c.execute("CREATE TABLE JobPostings (jobDescription TEXT, requirements TEXT, workLocation TEXT, salary DOUBLE, creationDate TEXT, selectedCandidate TEXT, PRIMARY KEY(jobKey), FOREIGN KEY(userID) REFERENCES LoginInfo(userKey))")
    # 
    descA = """Implement prototypes and software components, 
    Collaborate with team of excellent engineers to design, plan, develop, test, deliver and maintain complex features and new subsystems, 
    Participate and advise in code reviews"""
    reqsA = """Experience with large scale, distributed application design, 
    Detail oriented and passionate about building great software, 
    A constant desire to improve, learn more and take things to the next level, 
    Pursuing a BS or MS in Computer Science or related technical field, 
    Passion for building high quality software with extensive experience in unit testing and test driven development, 
    Excellent communication and writing skills, 
    Ability to operate effectively and independently in a dynamic, fluid environment"""

    descB="""Evolve within a devOps team
    Conduct design, development, code reviews and resolve production issues
    Be responsible for features from development to production"""
    reqsB="""Knowledge of Node.js and JavaScript development
    Knowledge of unit test libraries
    Knowledge of TypeScript
    Excellent communication and ownership skills
    Should be highly adaptive to ensure product and organizational agility.
    Experience in agile development and Scrum methodology."""
    

    descD = """Program code customized to the hardware you are working with
    Explore new hardware and deal with the interesting new challenges it poses
    Meet up with artists to assess their needs and vision
    Review code to improve its performance, in search of that vital extra millisecond
    You might attend a 3D tech talk by one of your colleagues on another project or brand – or give one yourself"""
    reqsD = """An undergraduate degree in Computer Science, Computer Engineering or equivalent
    A proficiency to communicate with all disciplines and to support and elevate the team in terms of visuals and performance
    Experience with HLSL, DirectXProficiency in C++ (understanding of C# is an asset)
    Experience developing on video-game consoles and in performance optimization for consoles
    You are a Philomath (a.k.a. a lover of maths – algebra, geometry, calculus, the whole set)
    You are creative and thirsty for innovation"""

    descE = """The pandemic has highlighted how important telecoms networks are to society. Nokia’s Network Infrastructure group is at the heart of a revolution to bring more and faster network capacity to people worldwide through our ambition, innovation, and technical expertise.
    Within the NI group, the WaveSuite team is building a new suite of applications that provides assurance, fulfillment, and analytics for telecommunication network providers/operators using state-of-the-art design and technologies."""
    reqsE = """Experience with UNIX/Linux environments.
    Solid knowledge of object oriented programming.
    Experience with Java 8, Node.js, front-end Angular or React, Scripting, Python"""
    
    descF = """evelop graphics programs using OpenGL and Vulkan
    Evaluate game performance on mobile device
    Prepare well-written and good quality report including research results
    Perform literature review on state-of-the-art approaches related to given tasks
    Efficient and timely communication/collaboration with other researchers from understanding a proposed method to its code implementation"""
    reqsF = """Currently enrolled in a university and registered with school’s co-op program
    Excellent communication skills, self-motivated, with creative thinking and attention to details
    Strong software development skills in Python and C/C++
    Familiarity with Linux, Windows and Github
    Understanding the concept of OpenGL, Vulkan and graphics pipeline
    Programming experience in OpenGL ES and/or Vulkan, or mobile game GPU programming"""

    insert1 = "INSERT INTO JobPostings VALUES (1, 2, 'Software Engineering Intern', 'MyCompany', '{desc}', '{reqs}', 'Montreal', 22.50,'None', '2023-03-18 20:59', 'None')".format(desc=descA, reqs=reqsA)
    insert2 = "INSERT INTO JobPostings VALUES (2, 2, 'Cloud Software Developer (Intern)', 'MyCompany', '{desc}', '{reqs}', 'Montreal', 25.00,'None', '2023-03-15 13:44', 'None')".format(desc=descB, reqs=reqsB)
    insert3 = "INSERT INTO JobPostings VALUES (3, 4, 'Developer Intern', 'YourCompany', '{desc}', '{reqs}', 'Ontario', 21.50,'None', '2023-03-19 14:25', 'None')".format(desc=descD, reqs=reqsD)
    insert4 = "INSERT INTO JobPostings VALUES (4, 4, 'Software Developer Co-Op', 'YourCompany', '{desc}', '{reqs}', 'Vancouver', 23.00,'None', '2023-03-19 14:25', 'None')".format(desc=descE, reqs=reqsE)
    insert5 = "INSERT INTO JobPostings VALUES (5, 4, 'Co-Op - Software Engineer', 'Your Company', '{desc}', '{reqs}', 'Edmonton', 27.00,'None', '2023-03-18 20:59', 'None')".format(desc=descF, reqs=reqsF)

    c.execute(insert1)
    c.execute(insert2)
    c.execute(insert3)
    c.execute(insert4)
    c.execute(insert5)

    #seventh table: feedback
    c.execute("CREATE TABLE userFeedback (feedbackKey NUMBER, feedback TEXT,userID NUMBER, email TEXT, PRIMARY KEY(feedbackKey)")


# testing - reading data from first table
finally:
    row=c.execute(
        "SELECT userKey, email, password, userType from LoginInfo").fetchall()
    print(row)
    profile=c.execute(
        "SELECT firstName, lastName, educInstitution, location from UserProfiles").fetchall()
    print(profile)
    # saves changes to the table
    conn.commit()
    c.close()
