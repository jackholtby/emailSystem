# A daily email system.

from flask import Flask, request, redirect, url_for
import schedule
import time
# from emaildb import updateStatus

app = Flask(__name__)

dashboardWrap = '''

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

    <table>
    <!-- email entries will go here -->
    %s

    </table>

  </div >
<!-- <script src="js/scripts.js"></script> -->
</body>
</html>
'''

emailEntry = '''
<tr class="email">
<td>%s</td>
<td>%s</td>
<td>%s</td>
</tr>
'''

@app.route('/', methods=['GET'])
def main():
    '''Main Dashboard Page.'''
    emails = "".join(emailEntry % (user_id, email_content) for user_id, email_content in get_emails())
    html = dashboardWrap & emails
    return html
