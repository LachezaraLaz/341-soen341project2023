#import flask into the file
from flask import Flask

#create flask object
app = Flask(__name__)

@app.route("/profile")
#home page
def home():
    return

#running flask app
if __name__ == "__main__":
    app.run()
