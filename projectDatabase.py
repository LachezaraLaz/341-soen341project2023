# import the built-in database
import sqlite3

# connection to the database module
conn = sqlite3.connect("data.db")

# checking that the database has been created
# print(conn.total_changes)

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
    c.execute("CREATE TABLE UserProfiles (profileKey NUMBER, userID NUMBER, contactInfo TEXT, portfolioLink TEXT, bio TEXT, skills TEXT, PRIMARY KEY (profileKey), FOREIGN KEY (userID) REFERENCES LoginInfo(userKey))")
    #third table: work experience table
    c.execute("CREATE TABLE WorkExperience (expKey NUMBER, profileID NUMBER, position TEXT, startMonth NUMBER, startYEAR NUMBER, endMonth NUMBER, endYear NUMBER, expDescription TEXT, skills TEXT, PRIMARY KEY(expKey), FOREIGN KEY(profileID) REFERENCES UserProfiles(profileKey))")
    #fourth table: job postings table
    c.execute("CREATE TABLE JobPostings (jobKey NUMBER, userID NUMBER, title TEXT, company TEXT, jobDescription TEXT, requirements TEXT, workLocation TEXT, salary DOUBLE, creationDate DATE, PRIMARY KEY(jobKey), FOREIGN KEY(userID) REFERENCES LoginInfo(userKey))")
    #inserting test data
    c.execute("INSERT INTO LoginInfo VALUES (1, 'test1@email.com', '123pass', 'student')")
    c.execute("INSERT INTO LoginInfo VALUES (2, 'test2@email.com', '1234pass', 'student')")

#testing - reading data from first table
finally:
    row = c.execute("SELECT userKey, email, password, userType from LoginInfo").fetchall()
    print(row)
    conn.commit()
    c.close()