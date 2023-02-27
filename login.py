#importing Flask and other modules
from flask import Flask, request, render_template

#Flask constructor which creates the Flask application object
app = Flask(__name__)

# A decorator used to tell the application which URL is associated function
@app.route('/login.html', methods =["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("form.html")
    else: #if the request method is POST
       # getting input with name = fname in HTML form
       email = request.form.get("email")
       # getting input with name = lname in HTML form
       password = request.form.get("password")
       return "Your email is "+ email + "Your password is "+ password

if(__name__ == '__main__'):
    app.run(debug=True)
