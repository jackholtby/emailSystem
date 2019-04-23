#!/bin/bash
# To setup the database for the system to work please do the following.

#Become root
su
# Enter root password.
# Alternatively just run the following with "sudo".

apt install postgresql

# make sure postgresql is running with: ps aux | grep postgresql
# log in as the postgres user
su - postgres

# This step isn't really necessary, but if you want to access the database
# and not have to use root, then it's useful.

# Create a user who has the same name as the user you use for your databasing.
# For example, my linux user is jack, and I so I created a user (ok, technically it's called a role) called jack:
createuser <INSERT CHOSEN USER NAME HERE>

# Now login to the postgres account and create the database.
su - postgres
create database emaildb

# Login as the user you created before. Navigate to the
# directory with the python server file and the Create-database.txt.
# Then run the following:
psql -d emaildb -f Create-database.txt

# And you should be set. Then run: python3 emailSystem.py
# The server is live at 0.0.0.0:8000
