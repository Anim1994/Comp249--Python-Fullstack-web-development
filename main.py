__author__ = 'Steve Cassidy'

from bottle import Bottle, template, static_file, debug, redirect
from interface import *
from users import *


app = Bottle()
debug(True)

@app.route('/')
def index(db):
    """This is the home page. The info contains the dictionary's itinerary. The values are then returned in to the template."""

    info = {
        'title': 'My Website',
        'message': 'Welcome to Jobs',
        'positions': position_list(db, 10),
        'usernick': session_user(db),
    }
    return template('index', info)

@app.post('/login')
def do_login(db):
    """This handles login submissions. The usernick and password is generated from the submission of the forms in the html page. The user is
    redirected to the homepage after login if it is successful. If login is unsuccessful the user is again given two forms to fill the credentials"""

    usernick = request.forms.get('nick')
    password = request.forms.get('password')

    check_login(db, usernick, password)             #check_login function checks whether the login is correct or not.
    if check_login(db,usernick,password) == True:
        generate_session(db, usernick)              #Creates a session for the user if login is successful.
        session_user(db)                            #Retrieves the user name from the database.
        return redirect('/')
    else:
        Z = {
            'title': 'Invalid',
            'message': 'Login Failed, please try again'
        }
        return template('loginform', Z)

@app.post('/post')
def do_submit(db):
    """this route handles the submission forms to create a position. If a user is successfully logged in then he will be able to create a position """

    usernick = session_user(db)                     #the usernick parameter is set to the output of session_user(db)

    title = request.forms.get('title')              #title,location,company,description are taken from the form submissions
    company = request.forms.get('company')
    location = request.forms.get('location')
    description = request.forms.get('description')

    position_add(db,usernick,title,location,company,description)    # this function takes these parameters and adds a position in the list

    return redirect('/')                            #redirects back to the homepage

@app.post('/logout')
def do_logout(db):
    """This handles the logout option."""

    usernick = session_user(db)
    delete_session(db,usernick)                     #the user session ends as its session entries are removed.

    return redirect('/')

@app.route('/about')
def about(db):
    """Contains the information of the about page."""

    x = {
        'title': 'About',
        'usernick': session_user(db),
        'message': "Jobs is a new, exciting, job posting service like nothing you've seen before!"
    }

    return template('about', x)

@app.route('/positions/01')
def position(db):
    """ page that contains all the details of a position"""
    read = {
        'title': 'Position 1',
        'positions': position_list(db),         #shows a list of positions that displays the latest 10.

    }

    return template('positions/01', read)

@app.route('/positions/02')
def position(db):
    """ page that contains all the details of a position"""
    read = {
        'title': 'Position 2',
        'positions': position_list(db)
    }

    return template('positions/02', read)

@app.route('/positions/03')
def position(db):
    """ page that contains all the details of a position"""
    read = {
        'title': 'Position 2',
        'positions': position_list(db)
    }

    return template('positions/02', read)

@app.route('/positions/03')
def position(db):
    """ page that contains all the details of a position"""
    read = {
        'title': 'Position 3',
        'positions': position_list(db)
    }

    return template('positions/03', read)

@app.route('/positions/04')
def position(db):
    """ page that contains all the details of a position"""
    read = {
        'title': 'Position 4',
        'positions': position_list(db)
    }

    return template('positions/04', read)

@app.route('/positions/05')
def position(db):
    """ page that contains all the details of a position"""
    read = {
        'title': 'Position 2',
        'positions': position_list(db)
    }

    return template('positions/05', read)

@app.route('/positions/06')
def position(db):
    """ page that contains all the details of a position"""
    read = {
        'title': 'Position 6',
        'positions': position_list(db)
    }

    return template('positions/06', read)

@app.route('/positions/07')
def position(db):
    """ page that contains all the details of a position"""
    read = {
        'title': 'Position 7',
        'positions': position_list(db)
    }

    return template('positions/07', read)

@app.route('/positions/08')
def position(db):
    """ page that contains all the details of a position"""
    read = {
        'title': 'Position 8',
        'positions': position_list(db)
    }

    return template('positions/08', read)

@app.route('/positions/09')
def position(db):
    """ page that contains all the details of a position"""
    read = {
        'title': 'Position 9',
        'positions': position_list(db)
    }

    return template('positions/09', read)

@app.route('/positions/10')
def position(db):
    """ page that contains all the details of a position"""
    read = {
        'title': 'Position 10',
        'positions': position_list(db)
    }

    return template('positions/10', read)

@app.route('/static/<filename:path>')
def static(filename):
    return static_file(filename=filename, root='static')


if __name__ == '__main__':

    from bottle.ext import sqlite
    from database import DATABASE_NAME, password_hash

    # install the database plugin
    app.install(sqlite.Plugin(dbfile=DATABASE_NAME))
    app.run(debug=True, port=8010)

