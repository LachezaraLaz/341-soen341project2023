# import database to connect and manage database
# flask to use Flask framework and
# request to handle HTML form requests
import sqlite3
from flask import Flask, request, render_template

# create Flask object
app = Flask(__name__)

#map route to signup  URL (tells Flask what URL triggers our following functions)
@app.route('/signup.html',methods = ['POST','GET'])
def signup():
    if request.method == "GET":
        return render_template('signUpHTML.html')
    elif request.method == "POST":
        # fetch email and password from form
        email = request.form['email']
        password = request.form['password']
        userType = request.form['userType']
        print("email is ",email)
        print("password is ", password)
        print(str(email[0:email.index("@")]),"hi")

        # connection to the database module
        conn = sqlite3.connect("data.db")
        c = conn.cursor()
        lastKey = c.execute("SELECT userKey FROM LoginInfo ORDER BY userKey DESC LIMIT 1").fetchone()[0]
        print("Key inside:",lastKey)

        # fetch row and store new record
        row = c.execute("SELECT userKey, email, password FROM LoginInfo").fetchall()
        lastKey = c.execute("SELECT userKey FROM LoginInfo ORDER BY userKey DESC").fetchone()[0]
        #newRecord = "INSERT INTO LoginInfo VALUES ("+str(lastKey+1)+","+str(email[0:email.index("@")])+","+str(password)+", 'employer')"
        newRecord = "INSERT INTO LoginInfo VALUES (" + str(lastKey+1) + ",\'" + str(email) + "\',\'" + str(password) + "\',\'" + str(userType) + "\')"

        #newRecord = "INSERT INTO LoginInfo VALUES ("+ str(lastKey+1)+", " + str("success test") + ", " + str(password) + ", 'testType')"
        row = c.execute(newRecord)
        conn.commit()
        c.close()
        return "sucess"




if(__name__ == '__main__'):
    app.run(debug=True)