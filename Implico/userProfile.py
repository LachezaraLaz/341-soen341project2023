#import flask into the file
from flask import Flask, Blueprint, render_template

userProfile = Blueprint('userprofile', __name__)

@userProfile.route('/profileHTML.html')
#home page
def home():
    return render_template('profileHTML.html')
