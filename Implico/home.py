#importing the sqlite3 module to handle database
import sqlite3
#importing Flask and other modules
from flask import Flask, request, render_template, redirect, session, Blueprint
from .signup import logout
#initializing blueprint
home = Blueprint('home', __name__)

# A decorator used to tell the application which URL is associated function
@home.route('/home.html', methods =['GET', 'POST'])
def beforeLogin():
    if request.method == 'GET':
        return render_template('home.html', boolean=True)    
    else:
        print("error")
    #if no POST request is made just stay on the login page
    return render_template('loginHTML.html', boolean=True)

@home.route('/indexEmployer.html', methods =['GET', 'POST'])
def afterLoginEmployer():
    if request.method == 'GET':
        return render_template('indexEmployer.html', boolean=True)
    #log out
    elif request.method == 'POST' and request.form.get("logout")!=None:
        logout()
        return render_template('home.html', boolean=True)
    else:
        print("error")
    #if no POST request is made just stay on the login page
    return render_template('indexEmployer.html', boolean=True)

@home.route('/indexAdmin.html', methods =['GET', 'POST'])
def afterLoginAdmin():
    if request.method == 'GET':
        return render_template('indexAdmin.html', boolean=True)
    #log out
    elif request.method == 'POST' and request.form.get("logout")!=None:
        logout()
        return render_template('home.html', boolean=True) 
    else:
        print("error")
    #if no POST request is made just stay on the login page
    return render_template('indexAdmin.html', boolean=True)

@home.route('/indexCandidate.html', methods =['GET', 'POST'])
def afterLoginCandidate():
    if request.method == 'GET':
        return render_template('indexCandidate.html', boolean=True)    
    #log out
    elif request.method == 'POST' and request.form.get("logout")!=None:
        logout()
        return render_template('home.html', boolean=True)
    else:
        print("error")
    #if no POST request is made just stay on the login page
    return render_template('indexCandidate.html', boolean=True)

@home.route('/aboutUs.html', methods=['GET', 'POST'])
def aboutUs():
    if request.method == 'GET':
        return render_template('aboutUs.html', boolean=True)    
    else:
        print("error")
    #if no POST request is made just stay on the login page
    return render_template('loginHTML.html', boolean=True)
