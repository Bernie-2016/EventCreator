import flask
from functions import create_events

app = flask.Flask(__name__)


# App Routes
@app.route('/')
def index():
    return flask.render_template('create_event.html', debug=app.debug)


@app.route('/create', methods=['POST'])
def create():
    # Log all the data sent from the form (for debugging purposes only)
    items = "\n"
    for key in flask.request.form:
        items += key + ' - ' + str(flask.request.form[key]) + '\n'
    app.logger.debug(items)

    response = create_events(flask.request.form)
    app.logger.debug(response)
    return response


if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=True)
