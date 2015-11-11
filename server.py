import flask
import flask.ext.login as flask_login

from functions import create_events
from functions import check_credentials
from functions import create_account

app = flask.Flask(__name__)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)



# Our mock database.
users = {'foo@bar.tld': {'pw': 'secret'}}

class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['pw'] == users[email]['pw']

    return user

# User management routes

@app.route('/create-account', methods=['GET', 'POST'])
def createaccount():
	if flask.request.method == 'GET':
		return flask.render_template('login.html')

	response = create_account(flask.request.form)
	app.logger.debug(response)

	return response

@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return '''
               <form action='login' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'></input>
                <input type='password' name='pw' id='pw' placeholder='password'></input>
                <input type='submit' name='submit'></input>
               </form>
               '''

    response = check_credentials(flask.request.form)
    app.logger.debug(response)

    return response

    email = flask.request.form['email']
    if flask.request.form['pw'] == users[email]['pw']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return flask.redirect(flask.url_for('protected'))

    return 'Bad login'

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'

@app.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'





# App Routes
@app.route('/')
def index():
	return flask.render_template('create_event.html', debug=app.debug)

@app.route('/create', methods=['POST'])
def create():
	items = "\n"
	for key in flask.request.form:
		items += key + ' - ' + str(flask.request.form[key]) + '\n'
	app.logger.debug(items)

	response = create_events(flask.request.form)

	app.logger.debug(response)
	return response

if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=True)
