"""
Created on Mar 26, 2012

@author: steve
"""
import uuid
from database import password_hash
from bottle import response,request
# this variable MUST be used as the name for the cookie used by this application
COOKIE_NAME = 'sessionid'


def check_login(db, usernick, password):
    """returns True if password matches stored"""
    cursor = db.cursor()
    sql = "Select nick, password From users"
    cursor.execute(sql)
    results = cursor.fetchall()

    for i in results:
        if i[0] == usernick:
            if i[1] == password_hash(password):
                return True
            return False

    return False


def generate_session(db, usernick):
    """create a new session and add a cookie to the response object (bottle.response)
    user must be a valid user in the database, if not, return None
    There should only be one session per user at any time, if there
    is already a session active, use the existing sessionid in the cookie
    """
    cursor = db.cursor()

    sql = "Select sessionid, usernick From sessions"
    cursor.execute(sql)
    result = cursor.fetchall()

    for row in result:
        if row[1] == usernick:
            response.set_cookie(COOKIE_NAME, row[0])
            return

    sessionid = uuid.uuid4().hex
    response.set_cookie(COOKIE_NAME, sessionid)
    sql1 = "INSERT INTO sessions (usernick, sessionid) VALUES (?,?)"
    cursor.execute(sql1, [usernick, sessionid])
    db.commit()

    sql2 = "Select usernick From sessions where sessionid = ?"
    cursor.execute(sql2, [sessionid])
    result = cursor.fetchone()

    for i in result:            #checks for invalid user
        if i[0] != usernick:
            return None


def delete_session(db, usernick):
    """remove all session table entries for this user"""
    cursor= db.cursor()

    sql = "Delete From sessions where usernick = ? "
    cursor.execute(sql, (usernick,))
    cursor.fetchall()



def session_user(db):
    """try to
    retrieve the user from the sessions table
    return usernick or None if no valid session is present"""

    cursor = db.cursor()
    sessionid = request.get_cookie(COOKIE_NAME)

    sql = "Select sessionid, usernick From sessions"
    cursor.execute(sql)
    result = cursor.fetchall()

    for row in result:
        if row[0] == sessionid:
            return row[1]

    return None
