import psycopg2, bleach
from datetime import datetime


# Set the database to access
DBNAME = "emaildb"

def allEmails():
    db = psycopg0.connect(database=DBNAME)
    c = db.cursor()
    c.execute("SELECT * FROM users;")
    for row in c:
        print(row[0])

def sendEmail(content, recipient):
    msg = EmailMessage()
    msg.set_content(content)
    msg['Subject'] = 'From The Admin'
    msg['From'] = 'admin@cooladminemail.com'
    msg['To'] = recipient

    s = smtplib.SMTP('localhost')
    s.send_message(msg)
    s.quit()

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

# Function addEmail():
# Inserts a new email into the emails table.
# Paramaters: user_id, email_contents.
def addEmail(user_id, email_content):
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("INSERT INTO emails (user_id, email_content, date_sent)", (bleach.clean(content),))
    db.commit();
    db.close()
