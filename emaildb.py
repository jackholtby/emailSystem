import psycopg2

DBNAME = "emaildb"

def sendEmails():
    # Sends out emails according to the status of each user.


def updateStatus():
    # Updates the state value for each user based on the following rules:
    # If user is 'Active' & last login more than 4 days ago: Mark "Not Responsive"
    # If user is 'Not responsive' & last login more than 2 days ago: Mark "Inactive"
    # If user is 'Not responsive' & last login less than 2 days ago: Mark "Active"

def getEmails():
    # Returns all entries in the emaildb database
    """Returns all emails from emaildb """
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select user_id, email_content, date_sent from emails order by time desc")
    posts = c.fetchall()
    db.close()
    return posts

def add_email():
