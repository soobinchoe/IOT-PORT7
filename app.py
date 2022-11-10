from authlib.integrations.flask_client import OAuth
from flask import Flask, redirect, session, url_for, render_template
from flask_cors import CORS

app = Flask(__name__)

app.secret_key = 'abcd'
CORS(app, supports_credentials=True)
oauth = OAuth(app)
github = oauth.register(
    name='github',
    client_id='a425fb9f00a8f2d7ce1b',
    client_secret='0752cee6e2e57f6cd4fe278030d406a2991c0023',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'},
)


@app.route('/')
def hello_world():
    user = dict(session).get('user', None)
    return render_template('main.html', user=user)


@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return github.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize():
    token = github.authorize_access_token()
    profile = github.get('/user', token=token).json()
    session['user'] = profile['login']
    return redirect('/')

@app.route('/logout')
def logout():
    session['user'] = None
    return redirect('/')

