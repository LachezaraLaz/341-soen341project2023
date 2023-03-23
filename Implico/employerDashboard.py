#importing the sqlite3 module to handle database
import sqlite3
#importing Flask and other modules
from flask import Flask, request, render_template, redirect, session, Blueprint
#initializing blueprint
employerDashboard = Blueprint('employerDashboard', __name__)

@employerDashboard.route('viewMoreJobEmployer.html', methods =['GET', 'POST'])
def func1():
    return

@employerDashboard.route('jobDashboardHTML.html', methods =['GET', 'POST'])
def func2():
    return

@employerDashboard.route('editJobEmployer.html', methods =['GET', 'POST'])
def func3():
    return   

@employerDashboard.route('jobApplicantsEmployer.html', methods =['GET', 'POST'])
def func4():
    return   