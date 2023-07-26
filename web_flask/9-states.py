#!/usr/bin/python3
"""
Starts a Flask web application that displays a list
of all State objects along with their linked City objects.
"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    """Removes the current SQLAlchemy Session."""
    storage.close()


@app.route('/states', strict_slashes=False)
def display_states():
    """Display a HTML page with the list of all State objects."""
    states = sorted(list(storage.all(State).values()), key=lambda x: x.name)
    return render_template('9-states.html', states=states)


@app.route('/states/<string:id>', strict_slashes=False)
def display_cities_by_state_id(id):
    """Display a HTML page with the list of City objects
    linked to a State."""
    state = storage.get(State, id)
    return render_template('9-states.html', state=state)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
