#!/usr/bin/python3
"""
Simple Flask webapplication that displayes "Hello HBNB!".
The application listens on 0.0.0.0, port 5000.

Routes:
    /: display "Hello HBNB!"
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
