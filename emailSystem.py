# A daily email system.

from flask import Flask, request, redirect, url_for
import schedule
import time
# from emaildb import updateStatus

app = Flask(__name__)

dashboardStart = '''

'''

dashbaoardEnd = '''

'''
