'''
This module will be a simple, dumb implementation of a Flask web app to serve
the index.html as a simple cut.

..module:: app
..modulauthor:: rfdoell
:synopsis: Dumb Flask server
'''

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def serve_index():
    return render_template('index.html')
