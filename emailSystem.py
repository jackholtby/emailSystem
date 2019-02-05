# A daily email system.

from flask import Flask, request, redirect, url_for
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
import time
from emaildb import getEmails, updateStatus, sendAllEmails, sendEmail

app = Flask(__name__)

# The function to send emails and update the database
def daily():
    updateStatus()
    sendAllEmails()
    # refresh dashboard

# The html for the dashboard for viewing the emails sent.
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
      Admin Email Dashboard
    </h1>

    <table class="email" border="1">
    <tr>
    <th> Recipient User ID</th>
    <th> Email Contents </th>
    <th> Date & Time Sent </th>
    </tr>

    <!-- email entries will go here -->
    %s

    </table>

  </div >
</body>
</html>
'''

# Email entry for dashboard. This is inserted into the dashboard html above.
emailEntry = '''\
<tr>
<td> %s </td>
<td> %s </td>
<td> %s </td>
</tr>
'''

scheduler = BackgroundScheduler()

scheduler.add_job(daily, 'cron', day='*', hour='18')

scheduler.start()

@app.route('/', methods=['GET'])
def main():
    '''Main Dashboard Page.'''
    emails = "".join(emailEntry % (user_id, email_content, date_sent) for user_id, email_content, date_sent in getEmails())
    html = dashboardWrap % emails
    return html

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8000)
