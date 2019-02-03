# A daily email system.


from flask import Flask, request, redirect, url_for
import schedule
import time
from emaildb import get_posts, add_post

app = Flask(__name__)

dashboardStart = '''

'''

dashbaoardEnd = '''

'''

def sendEmails():
    # Sends out emails according to the status of each userself.


def updateUserState():
    # Updates the state value for each user based on the following rules:
    # If user is 'Active' & last login more than 4 days ago: Mark "Not Responsive"
    # If user is 'Not responsive' & last login more than 2 days ago: Mark "Inactive"
    # If user is 'Not responsive' & last login less than 2 days ago: Mark "Active"
