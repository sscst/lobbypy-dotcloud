import os, re
from flask import (
        Flask,
        session,
        flash,
        redirect,
        )
from flask.ext.openid import OpenID

_steam_id_re = re.compile('steamcommunity.com/openid/id/(.*?)$')

app = Flask(__name__)
app.debug = True
app.secret_key = os.environ['SESSION_KEY']
oid = OpenID(app)

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/login')
@oid.loginhandler
def login():
    return oid.try_login('http://steamcommunity.com/openid')

@oid.after_login
def create_or_login(resp):
    match = _steam_id_re.search(resp.identity_url)
    session['user_id'] = match.group(1)
    flash('You are logged in as %s' % match.group(1))
    return redirect(oid.get_next_url())

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirct(oid.get_next_url())

if __name__ == '__main__':
    # Bind to port if defined, otherwise 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
