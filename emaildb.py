import psycopg2, bleach
from datetime import datetime


# Set the database to access
DBNAME = "emaildb"

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
    """Returns all emails from emaildb """
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select user_id, email_content, date_sent from emails order by time desc")
    emails = c.fetchall()
    db.close()
    return emails

# Insert a new email into the emails table.
# Paramaters: user_id and email_contents.
def add_email(user_id, email_content):
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("INSERT INTO emails (user_id, email_content, date_sent)", (%s, bleach.clean(content),))
    db.commit();
    db.close()
