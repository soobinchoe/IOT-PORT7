from authlib.integrations.flask_client import OAuth
from flask import Flask, redirect, session, url_for, render_template
from flask_cors import CORS
from sense_hat import SenseHat

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
    if user:
        # display_user(user)
        display_icon()
    return render_template('main.html', user=user)


def display_user(user):
    sense = SenseHat()
    sense.show_message(user)


def display_icon():
    sense = SenseHat()
    p = (255, 168, 168)  # pink
    b = (0, 0, 0)  # Black

    creeper_pixels = [
        b, b, b, b, b, b, b, b,
        b, b, p, b, b, p, b, b,
        b, p, b, p, p, b, p, b,
        b, p, b, b, b, b, p, b,
        b, p, b, b, b, b, p, b,
        b, b, p, b, b, p, b, b,
        b, b, b, p, p, b, b, b,
        b, b, b, b, b, b, b, b
    ]

    sense.set_pixels(creeper_pixels)


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


if __name__ == '__main__':
    app.run(host="pi-17.local", port=8000, debug=True)
