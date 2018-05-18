'''
This module will be a simple, dumb implementation of a Flask web app to serve
the index.html as a simple cut.

..module:: app
..modulauthor:: rfdoell
:synopsis: Dumb Flask server
'''

from flask import Flask, render_template

#pylint: disable=invalid-name
app = Flask(__name__)

@app.route('/')
def serve_index():
    '''
    This function will render the default html page and provide it to the user.

    :return: A rendered version of the index page
    :rtype: flask.Response
    '''
    return render_template('index.html')
