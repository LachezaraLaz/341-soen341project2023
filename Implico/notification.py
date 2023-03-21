import sqlite3
from flask import Flask, request, render_template, Blueprint, redirect
#initializing Blueprint
notification = Blueprint('notification', __name__)


@notification.route("/notification.html",methods = ['GET'])
def notif():
    if request.method == 'GET':
        return "hello" 