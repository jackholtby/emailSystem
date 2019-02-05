# A daily email system.

from flask import Flask, request, redirect, url_for
import schedule
import time
import smtplib
from email.message import EmailMessage
from emaildb import getEmails, updateStatus, addEmail, allEmails, sendEmail
# from emaildb import updateStatus

app = Flask(__name__)

def daily():
    updateStatus()
    allEmails()

dashboardWrap = '''\
<!DOCTYPE html>

<html lang="en">
<head>
  <meta charset="utf-8">

  <title></title>
  <meta name="description" content="Email System Dashboard">
  <meta name="author" content="Jack Holtby">

<link rel="stylesheet" href="main.css?v=1.0">

</head>

<body>

  <div id="flex-container">

    <h1>
      Dashboard
    </h1>

    <table class="email" border="1">
    <tr>
    <th> User ID</th>
    <th> Email Contents </th>
    <th> Date Sent </th>
    </tr>

    <!-- email entries will go here -->
    %s

    </table>

  </div >
</body>
</html>
'''

emailEntry = '''\
<tr>
<td> %s </td>
<td> %s </td>
<td> %s </td>
</tr>
'''

@app.route('/', methods=['GET'])
def main():
    '''Main Dashboard Page.'''
    emails = "".join(emailEntry % (user_id, email_content, date_sent) for user_id, email_content, date_sent in getEmails())
    print('emails variable content here:', emails)
    html = dashboardWrap % emails
    print(html)
    return html

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8000)
