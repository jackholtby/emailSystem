import psycopg2, bleach

# Set the database to access
DBNAME = "emaildb"

# Update the status of all users in the users table
def updateStatus():
    # Updates the state value for each user based on the following rules:
    # If user is 'Active' & last login more than 4 days ago: Mark "Not Responsive"
    # If user is 'Not responsive' & last login more than 2 days ago: Mark "Inactive"
    # If user is 'Not responsive' & last login less than 2 days ago: Mark "Active"

# Get all the emails from the emails table
def getEmails():
    # Returns all entries in the emaildb database
    """Returns all emails from emaildb """
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select user_id, email_content, date_sent from emails order by time desc")
    posts = c.fetchall()
    db.close()
    return posts

# Insert a new email into the emails table.
# Paramaters: user id and email contents.
def add_email(user_id, email_content):
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("insert into emails (user_id, email_content)", (%s, bleach.clean(content),))
    db.commit();
    db.close()
