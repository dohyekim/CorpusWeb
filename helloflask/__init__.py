from flask import Flask, render_template
from datetime import timedelta
from helloflask.init_db import init_database, db_session

app = Flask(__name__)
import helloflask.views
app.debug = True

app.config.update(
	# salt
    SECRET_KEY='X1243yRH!mMwf',
	SESSION_COOKIE_NAME='corpus_flask_session',
	PERMANENT_SESSION_LIFETIME=timedelta(31)      # 31 days
)

@app.before_first_request
def beforeFirstRequest():
    init_database()
# close connection
@app.teardown_appcontext
def teardown(exception):
    db_session.remove()
