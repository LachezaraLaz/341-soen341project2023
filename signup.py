# import database to connect and manage database
# flask to use Flask framework and
# request to handle HTML form requests
import sqlite3
from flask import Flask, request, render_template

# connection to the database module
conn = sqlite3.connect("data.db")
c = conn.cursor()
# create Flask object
app = Flask(__name__)


#map route to root URL (tells Flask what URL triggers our following functions)
@app.route('/signup',methods = ['POST','GET'])
def signup():
    if request.method == "GET":
        return render_template('signup.html')
    else:
        # fetch email and password from form
        email = request.form.get('email')
        password = request.form.get('password')
        
        row = c.execute("SELECT userKey, email, password FROM LoginInfo").fetchall()
        lastKey = c.execute("SELECT userKey FROM LoginInfo ORDER BY userKey DESC").fetchone()[0]
        #newRecord = "INSERT INTO LoginInfo VALUES ("+str(lastKey+1)+", 'test"+str(lastKey+1)+"@email.com', 'password"+str(lastKey+1)+"', 'employer')"
        newRecord = "INSERT INTO LoginInfo VALUES ("+ str(lastKey+1)+", " + str(email) + ", " + str(password) + ", 'testType')"
        row = c.execute(newRecord)




if(__name__ == '__main__'):
    app.run(debug=True)