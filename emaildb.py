import psycopg2, bleach
from datetime import datetime
from email.message import EmailMessage
import smtplib


# Set the database to access
DBNAME = "emaildb"

activeEmail = "Dear Sir or Madam, thank you for remaining active."

notResponsiveEmail = "Dear Sir or Madam, your status is not responsive. Login soon to become active."

sendFromEmail = 'admin@cooladminemail.com'

    # Function sendEmail()
    # Paramaters: content (of email), recipient
    # Sends an email to the provided email with the provided content.
    # Sending email is automatically: admin@cooladminemail.com
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

def sendAllEmails():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("SELECT * FROM users;")
    for row in c:
        if row[3] == 'active':
            sendEmail(activeEmail,row[2], row[0])

        elif row[3] == 'not responsive':
            emailSent = row[4].strftime("%Y-%m-%d %H:%M:%S")
            emailSent = datetime.strptime(emailSent, "%Y-%m-%d %H:%M:%S")
            now = datetime.now();
            difference = now - emailSent
            difference = difference.days
            if difference == 0 or difference == 3:
                sendEmail(notResponsiveEmail,row[2])
                addEmail(row[0], notResponsiveEmail)



# Update the status of all users in the users table
def updateStatus():
    # Updates the state value for each user based on the following rules:
    # If user is 'Active' & last login was more than 4 days ago: Mark "Not Responsive"
    # If user is 'Not responsive' & last login was more than 2 days ago: Mark "Inactive"
    # If user is 'Not responsive' & last login was less than 2 days ago: Mark "Active"

    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute('SELECT * FROM users')

    updateNotResponsive = '''
    UPDATE users
    SET status = 'not responsive'
    WHERE status = 'active'
    AND age(lastlogin::date) > '4 days';
    '''

    updateInactive = '''
    UPDATE users
    SET status = 'inactive'
    WHERE status = 'not responsive'
    AND age(lastlogin::date) > '2 days';
    '''

    updateActive = '''
    UPDATE users
    SET status = 'active'
    WHERE status = 'not responsive'
    AND age(lastlogin::date) < '2 days';
    '''

    c.execute(updateNotResponsive)
    c.execute(updateInactive)
    c.execute(updateActive)
    db.commit()
    db.close()


# Get all the emails from the emails table
def getEmails():
    # Returns all entries in the emaildb database
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("SELECT user_id, email_content, date_sent FROM emails ORDER BY date_sent DESC")
    emails = c.fetchall()
    db.close()
    return emails
