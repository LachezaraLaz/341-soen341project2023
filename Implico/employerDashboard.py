#importing the sqlite3 module to handle database
import sqlite3
#importing Flask and other modules
from flask import Flask, request, render_template, redirect, session, Blueprint
#initializing blueprint
employerDashboard = Blueprint('employerDashboard', __name__)

@employerDashboard.route('viewMoreJobEmployer.html', methods =['GET', 'POST'])
def fubctu():
    return

@employerDashboard.route('jobDashboardHTML.html', methods =['GET', 'POST'])
def fubctu():
    return

@employerDashboard.route('editJobEmployer.html', methods =['GET', 'POST'])
def fubctu():
    return   

@employerDashboard.route('jobApplicantsEmployer.html', methods =['GET', 'POST'])
def fubctu():
    return   