# A daily email system.
# Refers to emaildb.py for database accessing functions.

from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
import time
from emaildb import getEmails, updateStatus, sendAllEmails, sendEmail

app = Flask(__name__)

# The function to send emails and update the database
def daily():
    updateStatus()
    sendAllEmails()

# The html for the dashboard for viewing the emails sent.
dashboardWrap = '''\
<!DOCTYPE html>

<html lang="en">
<head>
  <meta charset="utf-8">

  <title>Admin Email Dashboard</title>
  <meta name="description" content="Email System Dashboard">
  <meta name="author" content="Jack Holtby">

</head>

<body>

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

    <p>
        Reload page after midnight to see new email records.
    </p>

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

# Setup background scheduler that sends the emails and updates
# the database every day at midnight.
scheduler = BackgroundScheduler()

scheduler.add_job(daily, 'cron', day='*', hour='0')

scheduler.start()

# And here we go... (Main App)
@app.route('/', methods=['GET'])
def main():
    # Generate the emails variable for inserting into the dashboard.
    emails = "".join(emailEntry % (user_id, email_content, date_sent) for user_id, email_content, date_sent in getEmails())
    # Insert the emails into the html variable for display.
    html = dashboardWrap % emails
    return html # And Viola! ;)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8000)
