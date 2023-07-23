#!/usr/bin/python3
"""
Flask web application with two routes.
The web application listens on 0.0.0.0, port 5000.

Routes:
    /: display "Hello HBNB!"
    /hbnb: display "HBNB"
    Mandatory use of `strict_slashes=False` in route definition.
"""
from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """
    Displays "Hello HBNB!" when accessing the root URL.
    """
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """
    Displays "HBNB" when accessing the '/hbnb' URL.
    """
    return 'HBNB'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
