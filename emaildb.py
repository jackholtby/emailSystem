# Name: emaildb
# Author: Jack Holtby
# Purpose: All database accessing functions used by the emailSystem.py file

import psycopg2, bleach
from datetime import datetime
from email.message import EmailMessage
import smtplib
import pandas

# Set the database to access
DBNAME = "emaildb"

# Email to be sent to active users
activeEmail = "Dear Sir or Madam. Thank you for remaining active."

# Email to be sent to not responsive users
notResponsiveEmail = "Dear Sir or Madam. Your status is not responsive. Login soon to become active."

# The email from which to send all emails.
sendFromEmail = 'admin@cooladminemail.com'

# Function sendEmail()
# Parameters: content (of email), recipient email, recipient user_id
# Sends an email to the provided email with the provided content.
def sendEmail(content, recipient, user_id):
    msg = EmailMessage()
    msg.set_content(content)
    msg['Subject'] = 'From The Admin'
    msg['From'] = sendFromEmail
    msg['To'] = recipient
    s = smtplib.SMTP('localhost')
    s.send_message(msg)
    s.quit()

    # Now updates the database to reflect the email just sent
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("INSERT INTO emails (user_id, email_content, date_sent) values (%s, %s, %s)", (user_id, bleach.clean(content), datetime.now()))
    c.execute("UPDATE users SET last_email_sent = %s WHERE user_id = %s", (datetime.now(), user_id))
    db.commit()
    db.close()


# Function: sendAllEmails()
# Parameters: None
# Sends out emails based on user status found in database.
# Note: This assumes that an email is sent at creation of each user.
# Otherwise we'd get empty columns and unhappy code...
def sendAllEmails():
    # Connect to the database.
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("SELECT * FROM users;")
    for row in c:
        # If they're active, send them an email.
        if row[3] == 'active':
            sendEmail(activeEmail, row[2], row[0])

        else:
            # Otherwise, setup a variable to check time since last email.
            emailSent = row[4].strftime("%Y-%m-%d %H:%M:%S")
            emailSent = datetime.strptime(emailSent, "%Y-%m-%d %H:%M:%S")
            now = datetime.now();
            difference = now - emailSent
            difference = difference.days

            # And last, if status is 'not responsive'
            # AND the days since the last email is a multiple of three,
            # then send a 'not responsive' email.
            if row[3] == 'not responsive' and (difference > 0 and difference % 3 == 0):
                sendEmail(notResponsiveEmail,row[2], row[0])

# Function: updateStatus()
# Parameters: None
# Updates the status of all users in the users table
def updateStatus():
    # Updates the state value for each user based on the following rules:
    # If user is 'Active' & last login was more than 4 days ago: Mark "Not Responsive"
    # If user is 'Not responsive' & last login was more than 2 days ago: Mark "Inactive"
    # If user is 'Not responsive' & last login was less than 2 days ago: Mark "Active"

    # Connect to the database
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()

    # Update for users who are not responsive and have not logged in for more than two days.
    # MUST BE DONE BEFORE updateNotResponsive
    updateInactive = '''
    UPDATE users
    SET status = 'inactive'
    WHERE status = 'not responsive'
    AND age(lastlogin::date) > '2 days';
    '''

    # Update statement for users who are active but have not logged in for more than 4 days
    updateNotResponsive = '''
    UPDATE users
    SET status = 'not responsive'
    WHERE status = 'active'
    AND age(lastlogin::date) > '4 days';
    '''

    # Update for users who are not responsive and have logged in within the last two days
    updateActive = '''
    UPDATE users
    SET status = 'active'
    WHERE status = 'not responsive'
    AND age(lastlogin::date) < '2 days';
    '''

    # Update the databases based on the three set update statements
    c.execute(updateInactive)
    c.execute(updateNotResponsive)
    c.execute(updateActive)
    db.commit()
    db.close()

# Function: getEmails
# Parameters: None
# Returns all the emails from the emails table ordered by date_sent
def getEmails():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("SELECT user_id, email_content, date_sent FROM emails ORDER BY date_sent DESC")
    emails = c.fetchall()
    db.close()
    return emails
