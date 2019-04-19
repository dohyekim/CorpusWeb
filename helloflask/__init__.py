from flask import Flask, render_template, url_for
from datetime import timedelta
from helloflask.init_db import init_database, db_session
import os

app = Flask(__name__)
import helloflask.views
app.debug = True

app.config.update(
	# salt
    SECRET_KEY='X1243yRH!mMwf',
	SESSION_COOKIE_NAME='corpus_flask_session',
	PERMANENT_SESSION_LIFETIME=timedelta(31)      # 31 days
)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)
    
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


@app.before_first_request
def beforeFirstRequest():
    init_database()
# close connection
@app.teardown_appcontext
def teardown(exception):
    db_session.remove()
