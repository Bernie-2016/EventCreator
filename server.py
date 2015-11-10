from flask import Flask
from flask import request
from flask import render_template

from functions import create_events

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('form.html', debug=app.debug)

@app.route('/create', methods=['POST'])
def create():
	items = "\n"
	for key in request.form:
		items += key + ' - ' + str(request.form[key]) + '\n'
	app.logger.debug(items)

	response = create_events(request.form)

	app.logger.debug(response)
	return response

if __name__ == '__main__':
    app.run(debug=True)