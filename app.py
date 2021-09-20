import os
import sqlite3
import spotipy
import time
import requests
import json
from flask import Flask, flash, redirect, render_template, url_for, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required, register_check, login_check
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint
import config

GOOGLE_MAP_API_KEY = config.GOOGLE_MAP_API_KEY
SPOTIFY_CLIENT_SECRET =config.SPOTIFY_CLIENT_SECRET
SPOTIFY_CLIENT_ID = config.SPOTIFY_CLIENT_ID

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Spotify用
app.secret_key = 'SOMETHING-RANDOM'
app.config['SESSION_COOKIE_NAME'] = 'spotify-login-session'

#use SQLite database
con = sqlite3.connect('spotify.db', check_same_thread=False)
db = con.cursor()

@app.route('/', methods = ['GET'])
@login_required
def index():
  return render_template('index.html')


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Forget any user_id
    session.clear()

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        username = request.form.get("username")
        
        used_email = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchall()

        # Ensure email, password, confirmation password, username was submitted
        if register_check(email, password, confirmation, username, used_email):
            # Insert user data
            db.execute("INSERT INTO users (email, hash, username) VALUES(?, ?, ?)", (email, generate_password_hash(password), username))
            con.commit()

            users = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchall()

            # Ensure username exists and password is correct
            if not check_password_hash(users[0][2], password):
                return render_template("register.html")

            session["user_id"] = users[0][1]
            # Redirect user to home page
            return redirect("/")
        else:
            return render_template("register.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        users = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchall()
        # Ensure email, password was submitted
        # Query database for username
        if login_check(email, password, users):
            # Ensure username exists and password is correct
            if not check_password_hash(users[0][2], password):
                return render_template("login.html")

            # Remember which user has logged in
            session["user_id"] = users[0][1]

            # Redirect user to home page
            return redirect("/")
        else:
            return render_template("login.html")
    # User reached route via GET (as by clicking a link or via redirect)
    else :
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/")

# Spotifyの認証ページへリダイレクト
@app.route('/spotify-login')
@login_required
def spotify_login():
    # def create_spotify_oauth()の情報を使いAPIでSpotifyオリジナルの認証ページを取得
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    # 取得したオリジナルページにリダイレクト
    return redirect(auth_url)

# Spotifyオリジナルの認証ページからの帰ってくる場所（SpotifyAPIの設定でこのLocalHost（127.0.0.1）で登録しているため、デプロイの際変更必要）
@app.route('/spotify-authorize')
@login_required
def spotify_authorize():
    sp_oauth = create_spotify_oauth()
    # session.clear()
    # 認証情報をsessionに保存
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session["token_info"] = token_info
    # 仮のページにリダイレクト（これが地図画面になる？）
    return redirect("/spotify-loading")

# Spotifyからログアウト（現在使っていない。もしspotifyだけログアウトしたいならtokeninfoだけsession消す必要あり。）
@app.route('/spotify-logout')
@login_required
def spotify_logout():
    session.clear() 
    return redirect('/')

@app.route('/spotify-loading')
@login_required
def spotify_loading():
    return render_template("loading.html")

# Spotfy認証後のリダイレクトページ
@app.route('/getTrack')
@login_required
def getTrack():

    # 認証しているかの確認
    session['token_info'], authorized = get_token()
    session.modified = True
    # していなかったらリダイレクト。
    if not authorized:
        return redirect('/')    
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    
    try:
        item = sp.current_playback()['item']['id']
        time.sleep(3) 
        current_track_info = get_current_track()
        # get_current_track()で取得したIDを1秒前に取得したものと比較して異なっていたら新しい曲とみなし書き込む。
        if current_track_info['id'] != session.get('current_id'):
            pprint(
            current_track_info,
            indent=4,
            )
        session['current_id'] = current_track_info['id']
        
        return redirect('/spotify-loading')
    except TypeError:
        return redirect("/spotify-loading")

# 現在再生されている曲情報を取得
def get_current_track():
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    id = sp.current_playback()['item']['id']
    track_name = sp.current_playback()['item']['name']
    artists = [artist for artist in sp.current_playback()['item']['artists']]
    link = sp.current_playback()['item']['href']
    image = sp.current_playback()['item']['album']['images'][2]['url']
    
    artist_names = ', '.join([artist['name'] for artist in artists])
    
    current_track_info = {
    	"id": id,
    	"track_name": track_name,
    	"artists": artist_names,
    	"link": link,
        "image": image
    }
    return current_track_info

# Spotify認証の保持の確認
# Checks to see if token is valid and gets a new token if not
def get_token():
    token_valid = False
    token_info = session.get("token_info", {})

    # Checking if the session already has a token stored
    if not (session.get('token_info', False)):
        token_valid = False
        return token_info, token_valid

    # Checking if token has expired
    now = int(time.time())
    is_token_expired = session.get('token_info').get('expires_at') - now < 60

    # Refreshing token if it has expired
    if (is_token_expired):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(session.get('token_info').get('refresh_token'))

    token_valid = True
    return token_info, token_valid

# SpotifyAPIを使うための情報
def create_spotify_oauth():
    return SpotifyOAuth(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
            redirect_uri=url_for('spotify_authorize', _external=True),
            scope="user-library-read, playlist-modify-public, playlist-modify-private, user-library-modify, playlist-read-private, user-library-read, user-read-recently-played, user-read-playback-state")

@app.route('/map', methods = ['GET'])
def display_map():
  googlemapURL = "https://maps.googleapis.com/maps/api/js?key="+GOOGLE_MAP_API_KEY
  print(googlemapURL)
  return render_template('map.html', GOOGLEMAPURL=googlemapURL)

if __name__ == '__main__':
  app.run(host=os.getenv('APP_ADDRESS', 'localhost'), port=5000)