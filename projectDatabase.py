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
    delRecord = "DELETE FROM LoginInfo WHERE userKey="+str(lastKey+1)
    delRow = c.execute(delRecord)


except sqlite3.OperationalError:
    # first table: login user table
    c.execute("CREATE TABLE LoginInfo (userKey NUMBER, email TEXT, password TEXT, userType TEXT, PRIMARY KEY (userKey))")
    # second table: candidate user profile info table
    c.execute("CREATE TABLE UserProfiles (profileKey NUMBER, userID NUMBER, firstName TEXT, lastName TEXT, bio TEXT, educInstitution TEXT, educDegree TEXT, location TEXT, contactInfo TEXT, portfolioLink TEXT, PRIMARY KEY (profileKey), FOREIGN KEY (userID) REFERENCES LoginInfo(userKey))")
    #third table: work experience table
    c.execute("CREATE TABLE WorkExperience (expKey NUMBER, profileID NUMBER, position TEXT, employer TEXT, startMonth NUMBER, startYEAR NUMBER, endMonth NUMBER, endYear NUMBER, expDescription TEXT, skills TEXT, PRIMARY KEY(expKey), FOREIGN KEY(profileID) REFERENCES UserProfiles(profileKey))")
    #fourth table: job postings table
    c.execute("CREATE TABLE JobPostings (jobKey NUMBER, userID NUMBER, title TEXT, company TEXT, jobDescription TEXT, requirements TEXT, workLocation TEXT, salary DOUBLE, creationDate DATE, PRIMARY KEY(jobKey), FOREIGN KEY(userID) REFERENCES LoginInfo(userKey))")
    #inserting test data in LoginInfo
    c.execute("INSERT INTO LoginInfo VALUES (1, 'test1@email.com', '123pass', 'student')")
    c.execute("INSERT INTO LoginInfo VALUES (2, 'test3@email.com', '1234pass', 'employer')")    
    c.execute("INSERT INTO LoginInfo VALUES (3, 'test2@email.com', '12345pass', 'student')")
    c.execute("INSERT INTO LoginInfo VALUES (4, 'test3@email.com', '123456pass', 'employer')")
    c.execute("INSERT INTO LoginInfo VALUES (5, 'admin@email.com', '1234567pass', 'admin')")

    #inserting test data in UserProfiles
    c.execute("INSERT INTO UserProfiles VALUES (1, 1, 'Jane', 'Doe', 'I am a second year Software Engineering student looking to further my career options', 'Concordia University', 'Software Engineering', 'Montreal', 'test1@email.com', 'github.com')")
    c.execute("INSERT INTO UserProfiles VALUES (2, 3, 'John', 'Doe', 'I am a third year Computer Science student and my code is out of this world', 'UQAM', 'Computer Science', 'Montreal', '111-222-3333', 'github.com/git_name')")

    #inserting test data in WorkExperience
    c.execute("INSERT INTO WorkExperience VALUES (1, 1, 'Developer Intern', 'BOM.B', 1, 2022, 5, 2022, 'develop website', 'HTML, CSS, JS, C#')")
    c.execute("INSERT INTO WorkExperience VALUES (2, 1, 'Cashier', 'Food Store', 4, 2019, 5, 2022, 'working in customer service at a grocery store', 'POST, Communication, Attentive')")
    c.execute("INSERT INTO WorkExperience VALUES (3, 3, 'Developer Intern', 'BOM.B', 1, 2022, 5, 2022, 'develop website', 'HTML, CSS, JS, C#')")
    c.execute("INSERT INTO WorkExperience VALUES (4, 3, 'Cashier', 'Food Store', 4, 2019, 5, 2022, 'working in customer service at a grocery store', 'POST, Communication, Attentive')")


#testing - reading data from first table
finally:
    row = c.execute("SELECT userKey, email, password, userType from LoginInfo").fetchall()
    print(row)
    profile = c.execute("SELECT firstName, lastName, educInstitution, location from UserProfiles").fetchall()
    print(profile)
    #saves changes to the table
    conn.commit()
    c.close()