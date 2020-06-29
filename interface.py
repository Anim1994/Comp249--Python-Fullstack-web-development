"""
Database Model interface for the COMP249 Web Application assignment

@author: steve cassidy
"""

import sqlite3
from time import gmtime, strftime

def position_list(db, limit=10):
    """Return a list of positions ordered by date
    db is a database connection
    return at most limit positions (default 10)

    Returns a list of tuples  (id, timestamp, owner, title, location, company, description)
    """
    cursor = db.cursor()

    sql = 'Select id, timestamp, owner, title, description From positions order by timestamp desc'

    cursor.execute(sql)
    """result = []"""

    return cursor.fetchmany(limit)


def position_get(db, id):
    """Return the details of the positions with the given id
    or None if there is no positions with this id

    Returns a tuple (id, timestamp, owner, title, location, company, description)

    """
    cursor = db.cursor()
    sql = 'select id,timestamp,owner,title,location,company,description from positions'
    cursor.execute(sql)

    for row in cursor.fetchall():
        if row[0] == id:
            return row

    return None

def position_add(db, usernick, title, location, company, description):
    """Add a new post to the database.
    The date of the post will be the current time and date.
    Only add the record if usernick matches an existing user

    Return True if the record was added, False if not."""

    cursor = db.cursor()
    cursor.execute('Select owner from positions')

    found = False

    for name in cursor.fetchall():
        if name[0] == usernick:
            found = True

    if found == False:
        return False

    timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())

    sql = "Insert into positions (timestamp,owner,title,location,company,description) VALUES (?,?,?,?,?,?)"
    cursor.execute(sql, (timestamp,usernick, title, location, company, description))
    db.commit()

    return True




