# import the built-in database
import sqlite3

# connection to the database module
conn = sqlite3.connect("data.db")

# allow for SQL commands to be run
c = conn.cursor()

#check if the database tables have been made
try:
    row = c.execute("SELECT userKey, email, password FROM LoginInfo").fetchall()
    lastKey = c.execute("SELECT userKey FROM LoginInfo ORDER BY userKey DESC").fetchone()[0]
    newRecord = "INSERT INTO LoginInfo VALUES ("+str(lastKey+1)+", 'test"+str(lastKey+1)+"@email.com', 'password"+str(lastKey+1)+"', 'employer')"

    row = c.execute(newRecord)


except sqlite3.OperationalError:
    # first table: login user table
    c.execute("CREATE TABLE LoginInfo (userKey NUMBER, email TEXT, password TEXT, userType TEXT, PRIMARY KEY (userKey))")
    # second table: candidate user profile info table
    c.execute("CREATE TABLE UserProfiles (profileKey NUMBER, userID NUMBER, firstName TEXT, lastName TEXT, bio TEXT, education TEXT, location TEXT, contactInfo TEXT, portfolioLink TEXT, PRIMARY KEY (profileKey), FOREIGN KEY (userID) REFERENCES LoginInfo(userKey))")
    #third table: work experience table
    c.execute("CREATE TABLE WorkExperience (expKey NUMBER, profileID NUMBER, position TEXT, startMonth NUMBER, startYEAR NUMBER, endMonth NUMBER, endYear NUMBER, expDescription TEXT, skills TEXT, PRIMARY KEY(expKey), FOREIGN KEY(profileID) REFERENCES UserProfiles(profileKey))")
    #fourth table: job postings table
    c.execute("CREATE TABLE JobPostings (jobKey NUMBER, userID NUMBER, title TEXT, company TEXT, jobDescription TEXT, requirements TEXT, workLocation TEXT, salary DOUBLE, creationDate DATE, PRIMARY KEY(jobKey), FOREIGN KEY(userID) REFERENCES LoginInfo(userKey))")
    #inserting test data in LoginInfo
    c.execute("INSERT INTO LoginInfo VALUES (1, 'test1@email.com', '123pass', 'student')")
    c.execute("INSERT INTO LoginInfo VALUES (2, 'test2@email.com', '1234pass', 'student')")
    #inserting test data in UserProfiles
    c.execute("INSERT INTO UserProfiles VALUES (1, 1, 'Megan', 'Coscia', 'I am a second year Software Engineering students looking to further my career options', 'Software Engineering', 'Montreal', 'test1@email.com', 'github.com')")
    #inserting test data in WorkExperience
    c.execute("INSERT INTO WorkExperience VALUES (1, 1, 'Developer Intern', 1, 2022, 5, 2022, 'develop website', 'HTML, CSS, JS, C#')")

#testing - reading data from first table
finally:
    row = c.execute("SELECT userKey, email, password, userType from LoginInfo").fetchall()
    print(row)
    profile = c.execute("SELECT firstName, lastName, education, location from UserProfiles").fetchall()
    print(profile)
    #saves changes to the table
    conn.commit()
    c.close()