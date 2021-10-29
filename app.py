import os
from re import S
import sqlite3

from flask.wrappers import Request
from requests.api import get
# from typing import AwaitableGenerator, Text
import spotipy
import time
import datetime
import requests
import json
from flask import Flask, flash, redirect, render_template, url_for, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required, register_check, login_check
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint
import config
from models import users, song_locations, songs, follow, made_playlists, Group, UserGroup, requests, likes, db
from sqlalchemy import or_, desc, and_, distinct
from sqlalchemy.sql import func, exists

from profile import Profile_info
from home import Home_info
import random


GOOGLE_MAP_API_KEY = config.GOOGLE_MAP_API_KEY
SPOTIFY_CLIENT_SECRET =config.SPOTIFY_CLIENT_SECRET
SPOTIFY_CLIENT_ID = config.SPOTIFY_CLIENT_ID

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.secret_key = 'SOMETHING-RANDOM'
app.config['SESSION_COOKIE_NAME'] = 'session-id'

#database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
db.app = app

db.create_all()
print("table is created")

@app.route('/', methods = ['GET'])
@login_required
def index():
    session['token_info'], authorized = get_token()
    session.modified = True
    # していなかったらリダイレクト。
    if not authorized:
        return redirect('/spotify-login')    
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    # マップ表示
    googlemapURL = "https://maps.googleapis.com/maps/api/js?key="+GOOGLE_MAP_API_KEY
    pins = []
    songdata = []
    
    # 自分のピン表示
    # pins = db.session.query(song_locations).filter(song_locations.user_id == session["user_id"]).all()
    follow_users = db.session.query(follow.followed_user_id).filter(follow.follow_user_id == session["user_id"]).all()
    for follow_user in follow_users:
        # print(follow_user)
        follow_pins = db.session.query(song_locations).filter(song_locations.user_id == follow_user[0]).filter(song_locations.is_private == "False").all()
        for follow_pin in follow_pins:
            pins.append(follow_pin)
    for pin in pins:
        # print(pin)
        song = db.session.query(songs).filter(songs.track_id == pin.track_id).first()
        user = db.session.query(users).filter(users.id == pin.user_id).first()
        # print(user.nickname)
        songdata.append({'id':pin.id,'lat':pin.latitude, 'lng':pin.longitude, 'date':pin.date.strftime("%Y-%m-%d"),
        'artist':song.artist_name, 'track':song.track_name, 'image':song.track_image ,'link':song.spotify_url, 'user_id':pin.user_id, 'emotion':pin.emotion, 'about':pin.about, 'comment':pin.comment, 'is_private':pin.is_private, 'user_nickname':user.nickname, 'track_id':pin.track_id})

    #最新3件の投稿をリスト表示させる
    latestpins = []
    latestsongdata = []
    # latestpins = db.session.query(song_locations).filter(song_locations.user_id == session["user_id"]).limit(3).all()

    for follow_user in follow_users:
        latestfollow_pins = db.session.query(song_locations).filter(song_locations.user_id == follow_user[0]).order_by(desc(song_locations.id)).limit(3).all()
        for follow_pin in latestfollow_pins:
            latestpins.append(follow_pin)
    for pin in latestpins:
            # print(pin)
            song = db.session.query(songs).filter(songs.track_id == pin.track_id).first()
            user = db.session.query(users).filter(users.id == pin.user_id).first()
            # print(user.nickname)
            # latestsongdata.append({'id':pin.id,'lat':pin.latitude, 'lng':pin.longitude, 'date':pin.date.strftime("%Y-%m-%d"),
            # 'artist':song.artist_name, 'track':song.track_name, 'image':song.track_image ,'link':song.spotify_url, 'track_id':song.track_id, 'user_id':pin.user_id, 'emotion':pin.emotion, 'about':pin.about, 'comment':pin.comment, 'is_private':pin.is_private, 'user_nickname':user.nickname})
#いいね判定 
            if db.session.query(exists().where(likes.song_location_id == pin.id).where(likes.user_id == session['user_id'])).scalar() == True:
                print("True")
                latestsongdata.append({'like':'yes','id':pin.id,'lat':pin.latitude, 'lng':pin.longitude, 'date':pin.date.strftime("%Y-%m-%d"),
                'artist':song.artist_name, 'track':song.track_name, 'image':song.track_image ,'link':song.spotify_url, 'track_id':song.track_id, 'user_id':pin.user_id, 'emotion':pin.emotion, 'about':pin.about, 'comment':pin.comment, 'is_private':pin.is_private, 'user_nickname':user.nickname})
            else:
                latestsongdata.append({'like':'no','id':pin.id,'lat':pin.latitude, 'lng':pin.longitude, 'date':pin.date.strftime("%Y-%m-%d"),
                'artist':song.artist_name, 'track':song.track_name, 'image':song.track_image ,'link':song.spotify_url, 'track_id':song.track_id, 'user_id':pin.user_id, 'emotion':pin.emotion, 'about':pin.about, 'comment':pin.comment, 'is_private':pin.is_private, 'user_nickname':user.nickname})


    return render_template('index.html',user_id=session["user_id"] , GOOGLEMAPURL=googlemapURL ,Songdatas=songdata,latestsongdata=latestsongdata)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Forget any user_id
    session.pop("user_id", None)
    print("register")

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        nickname = request.form.get("nickname")
        
        used_email = db.session.query(users).filter(users.username == username).all()
        if used_email != []:
            print(used_email[0].username)
            print("is used username")

        # Ensure username, password, confirmation password, nickname was submitted
        if register_check(username, password, confirmation, nickname, used_email):
            # Insert user data
            
            new_user = users(username=username, hash=generate_password_hash(password), nickname=nickname)
            db.session.add(new_user)
            db.session.commit()

            users_row = db.session.query(users).filter(users.nickname == nickname).all()
            print(users_row[0].username)
            print("is new user username")

            # Ensure nickname exists and password is correct
            if not check_password_hash(users_row[0].hash, password):
                return render_template("register.html")

            session["user_id"] = users_row[0].id
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
    session['current_id']=None
    session.pop("user_id", None)
    print("login")

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        users_row = db.session.query(users).filter(users.username == username).all()
        if users_row != []:
            print(users_row[0].username)
            print("is login username")

        # Ensure username, password was submitted
        # Query database for nickname
        if login_check(username, password, users_row):
            # Ensure nickname exists and password is correct
            if not check_password_hash(users_row[0].hash, password):
                return render_template("login.html")

            # Remember which user has logged in
            session["user_id"] = users_row[0].id

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
    session.pop("user_id", None)
    
    # Redirect user to login form
    return redirect("/")



@app.route('/profile/<display_user_id>', methods = ['GET','POST'])
@login_required
def profile(display_user_id):
    session['token_info'], authorized = get_token()
    session.modified = True
    # Spotify認証していなかったらリダイレクト。
    if not authorized:
        return redirect('/spotify-login')    
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))

    # ユーザの情報
    login_user_id = session["user_id"]
    track_ids = db.session.query(song_locations.track_id).filter(song_locations.user_id == display_user_id).all()
    username = db.session.query(users.username).filter(users.id == display_user_id).first()
    nickname = db.session.query(users.nickname).filter(users.id == display_user_id).first()
    print("login_user_id: ", end="")
    print(login_user_id)
    print("username: ", end="")
    print(username[0])
    print(nickname[0])

    # マップ表示
    googlemapURL = "https://maps.googleapis.com/maps/api/js?key="+GOOGLE_MAP_API_KEY
    pins = []
    songdata = []
    display_user_id = int(display_user_id)
    if login_user_id != display_user_id:
        pins = db.session.query(song_locations).filter(song_locations.user_id == display_user_id).filter(song_locations.is_private == "False").all()
        print("diff")
    elif login_user_id == display_user_id:
        pins = db.session.query(song_locations).filter(song_locations.user_id == display_user_id).all()
        print("same")
    else:
        print("error")
    
    for pin in pins:
        song = db.session.query(songs).filter(songs.track_id == pin.track_id).first()
        songdata.append({'id':pin.id,'lat':pin.latitude, 'lng':pin.longitude, 'date':pin.date.strftime("%Y-%m-%d"),
        'artist':song.artist_name, 'track':song.track_name, 'image':song.track_image ,'link':song.spotify_url, 'user_id':pin.user_id, 'emotion':pin.emotion, 'about':pin.about, 'comment':pin.comment, 'is_private':pin.is_private})
        
    #最新3件の投稿を表示させる
    latestpins = []
    latestsongdata = []
    if login_user_id != display_user_id:
        latestpins = db.session.query(song_locations).filter(song_locations.user_id == display_user_id).filter(song_locations.is_private == "False").order_by(desc(song_locations.id)).limit(3).all()
        print("diff")
    elif login_user_id == display_user_id:
        latestpins = db.session.query(song_locations).filter(song_locations.user_id == display_user_id).order_by(desc(song_locations.id)).limit(3).all()
        print("same")
    else:
        print("error")
    for pin in latestpins:
        song = db.session.query(songs).filter(songs.track_id == pin.track_id).first()
        user = db.session.query(users).filter(users.id == pin.user_id).first()
        latestsongdata.append({'id':pin.id,'lat':pin.latitude, 'lng':pin.longitude, 'date':pin.date.strftime("%Y-%m-%d"),
        'artist':song.artist_name, 'track':song.track_name,'track_id': pin.track_id, 'image':song.track_image ,'link':song.spotify_url, 'user_id':pin.user_id, 'emotion':pin.emotion, 'about':pin.about, 'comment':pin.comment, 'is_private':pin.is_private, 'user_nickname':user.nickname})
        # print("latest",latestsongdata)

    following_status = ""
    # 表示しているユーザーのフォロー情報
    display_user_id = int(display_user_id) # int型に統一
    if display_user_id == login_user_id:
        following_status = "myself"
    else:
        following = db.session.query(follow).filter(follow.follow_user_id == login_user_id, follow.followed_user_id == display_user_id).first()
        if following:
            following_status = "True"
        else:
            following_status = "False"

    # フォローフォロワー数
    follow_user = db.session.query(follow).filter(follow.follow_user_id == display_user_id).all()
    if follow_user:
        follow_number = len(follow_user)
    else: 
        follow_number = 0

    followed_user = db.session.query(follow).filter(follow.followed_user_id == display_user_id).all()
    if followed_user:
        followed_number = len(followed_user)
    else:
        followed_number = 0

    songlists = []
    for track_id in track_ids:
        songlists.append(db.session.query(songs.track_name, songs.artist_name, songs.track_image, songs.spotify_url).filter(songs.track_id == track_id[0]).first())
    
    user_info = dict(id=display_user_id, username=username[0], following=following_status, follow_number=follow_number, followed_number=followed_number, songlists=songlists, nickname=nickname[0])
    
    # 自己紹介文取得
    if db.session.query(users.introduce).filter(users.id == display_user_id).all()[0][0] != None:
        Introduce = db.session.query(users.introduce).filter(users.id == display_user_id).all()[0][0]
    else:
        Introduce ="Settingで自己紹介入力してください"
    
    
    if request.method == "GET":
        #地図とかただ表示させるだけ
        return render_template('profile.html', user_id=login_user_id ,user_info=user_info, GOOGLEMAPURL=googlemapURL ,Songdatas=songdata, latestsongdata=latestsongdata,  Introduce = Introduce) 
    if request.method == "POST":
        #playlist作成ボタン押したときmakeplaylistにデータ渡す
        playlist_name = request.form['playlistname']
        return render_template('makeplaylist.html', data = songdata, name = playlist_name, user_id = session['user_id'])

# 自己紹介文更新
@app.route('/setting', methods = ['GET','POST'])
@login_required
def setting():
    if request.method == 'GET':
        return render_template('setting.html',user_id=session['user_id'])
    else:
        text = request.form.get("text")
        user = users.query.filter_by(id=session['user_id']).first()
        user.introduce=text
        db.session.commit()
        return redirect(url_for('profile', display_user_id=session['user_id']))

@app.route('/follow', methods = ['POST'])
@login_required
# profile->follow->home
def following():
    operator = session["user_id"]
    operated = request.form.get("user_id")
    follow_or_cancell = request.form.get("follow_or_cancell")
    if operator != operated:
        if follow_or_cancell == "follow":
            new_follow = follow(follow_user_id=operator, followed_user_id=operated)
            db.session.add(new_follow)
            db.session.commit()
            print("follow", end=": ")
            print(operated)
            rows = db.session.query(follow).all()
            for row in rows:
                print(row.follow_user_id, end="->")
                print(row.followed_user_id)
        elif follow_or_cancell == "cancell":
            # 指定したデータを削除
            delete_follows = db.session.query(follow).filter_by(follow_user_id=operator, followed_user_id=operated).all()
            print(delete_follows)
            for delete_follow in delete_follows:
                db.session.delete(delete_follow)
            db.session.commit()
            print("cancell", end=": ")
            print(operated)
            rows = db.session.query(follow).all()
            for row in rows:
                print(row.follow_user_id, end="->")
                print(row.followed_user_id)
        else:
            print("error")
            return redirect("/")
        
        return redirect("/")
        
        # マップ表示
        # googlemapURL = "https://maps.googleapis.com/maps/api/js?key="+GOOGLE_MAP_API_KEY
        # pins = []
        # songdata = []
        # display_user_id = operated
        # pins = db.session.query(song_locations).filter(song_locations.user_id == display_user_id).all()
        
        # for pin in pins:
        #     song = db.session.query(songs).filter(songs.track_id == pin.track_id).first()
        #     songdata.append({'id':pin.id,'lat':pin.latitude, 'lng':pin.longitude, 'date':pin.date.strftime("%Y-%m-%d"),
        #     'artist':song.artist_name, 'track':song.track_name, 'image':song.track_image ,'link':song.spotify_url, 'user_id':pin.user_id, 'emotion':pin.emotion, 'comment':pin.comment})
        #     print(pin.date)


        # user_info = dict(id=display_user_id, name="ma-")
        # return render_template('profile.html',login_user_id=session["user_id"] ,user_info=user_info, GOOGLEMAPURL=googlemapURL ,Songdatas=songdata)
        
    else:
        print("error")
        return redirect("/profile")
        # return render_template('profile.html') 

@app.route('/search', methods = ['GET'])
@login_required
def search():
    session['token_info'], authorized = get_token()
    session.modified = True
    # していなかったらリダイレクト。
    if not authorized:
        return redirect('/spotify-login')    
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    # #ユーザ検索
	# まずはログインユーザのもってるアーティストリストを出す。
    artistslist = []
    artistimage=[]
    artistsdata = db.session.query(songs.artist_name, songs.track_id).filter(songs.track_id == song_locations.track_id).filter(song_locations.user_id == session["user_id"]).all()
    #artists = db.session.query(songs.artist_name, songs.track_image, songs.track_name).filter(songs.track_id == song_locations.track_id).filter(song_locations.user_id == session["user_id"]).all()
    artist_name = set([])
    for artist in artistsdata:
        print("artist",artist[0])
        len1 = len(artist_name)
        artist_name.add(artist[0])
        len2 = len(artist_name)
        len1 += 1
        if len1 == len2:
            artistslist.append(dict(image=sp.artist(sp.track(artist[1])["album"]['artists'][0]['id'])['images'][2]['url'], name=artist[0]))

    print(artistslist)

    
    # for artist in artistsdata:
    #     print("id",artist[1])
    #     print("いっこめ",sp.track(artist[1])["album"]['artists'][0]['id'])
    #     # sptrack_id.append(artist[1])
    #     print("art",sp.artist(sp.track(artist[1])["album"]['artists'][0]['id'])['images'][2]['url'])

    # print(artistslist)
    # for artist in artistslist:
    #     print(artist)

    #  
    # for artistdata in artistsdata:
    #     print(artistdata[0]) 
    #     # print(artistdata.track_name)
    #     print(artistdata[2])
    #     # print (artistname.replace("(","").replace(")","").replace("'",""))
    #     artistslist.append(artistdata[0])

    # artist_info = []
    # for artistdata in artistsdata:
    #     artist_info.append(artistdata)

    # newartistlist =[]
    # # print(artistslist.replace("(","").replace(")","").replace("'",""))
    # for artist in artistslist:
    #     artist = artist.replace("(","").replace(")","").replace("'","")
    #     print(artist)
    #     newartistlist.append({'artistname':artist})

    return render_template('search.html',user_id=session["user_id"],artistslist=artistslist)
    # return render_template('search.html',user_id=session["user_id"],artistslist=artistslist, artist_info=artist_info)


@app.route('/search/<selectedartistname>', methods = ['GET'])
@login_required
def searchuser(selectedartistname):
    # __tablename__ = 'users'
	# id = db.Column(Integer, primary_key=True) これを含んだURLが飛ばせればよい。

    print(selectedartistname)
    userlist = set([])
    trackdata = db.session.query(songs.track_id).filter(songs.artist_name == selectedartistname).all()
    # userdata = db.session.query(songs.artist_name).filter(songs.artist_name == selectedartistname).all()
    # userdata = db.session.query(songsn)

    for track in trackdata:
        userdata = db.session.query(song_locations.user_id).filter(song_locations.track_id == track[0]).all()
        for id in userdata:
            userlist.add(id[0])
    
    user_info = []
    for user in userlist:
        user_info.append(db.session.query(users.id, users.username, users.nickname).filter(users.id == int(user)).first())
    print(userlist)     
    return render_template('search.html',userlist=userlist, user_info=user_info, user_id=session["user_id"])


@app.route('/search/id/<nickname>', methods = ['GET'])
@login_required
def searchId(nickname):
    # __tablename__ = 'users'
	# id = db.Column(Integer, primary_key=True) これを含んだURLが飛ばせればよい。

    searchId = db.session.query(users.id).filter(users.nickname == nickname).first()
    # print(searchId)
    username = db.session.query(users.username).filter(users.nickname == nickname).first()
    # nickname = db.session.query(users.nickname).filter(users.id == searchId).first()
    
    return render_template('search.html',username=username[0], nickname=nickname,searchId=searchId[0], user_id=session["user_id"])


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
    return redirect("/")

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
@app.route('/getTrack', methods = ['POST'])
@login_required
def getTrack():
    #認証しているか確認
        session['token_info'], authorized = get_token()
        session.modified = True
        # していなかったらリダイレクト。
        if not authorized:
            return redirect('/spotify-login')    
        sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
        try:
            # 連続で取得すると、エラーするため少し時間を置く（今は問題なさそうだからコメントアウト）
            # time.sleep(3) 
            current_track_info = get_current_track()
            
            # POSTの受け取り
            lat = request.form.get('lat')
            lng = request.form.get('lng')
            emotion = request.form.get('emotion')
            comment = request.form.get('comment')
            pin_status = request.form.get('pin_status')
            is_private = ""
            if pin_status == "private":
                is_private = "True"
            elif pin_status == "public":
                is_private = "False"
            # print(pin_status)
            # print(is_private)

            # addingで日付受け取った場合
            if request.form.get('date'): 
                date_str = request.form.get('date')
                Datetime = datetime.datetime.strptime(date_str, "%Y-%m-%d")
                date = Datetime.date()
            # loadingで現在地追加の日付を使う場合
            else:
                date = datetime.date.today()
                # Datetime = datetime.datetime.now()
            # get_current_track()で取得したIDを以前取得したものと比較して異なっていたら新しい曲とみなし書き込む。
            if current_track_info['id'] != session.get('current_id'):
                exist_song = db.session.query(songs).filter(songs.track_id == current_track_info["id"]).all()
                if exist_song == []:
                    print(current_track_info["artists"])
                    new_song = songs(track_id=current_track_info["id"], track_name=current_track_info["track_name"], artist_name=current_track_info["artists"], track_image=current_track_info["image"], spotify_url=current_track_info["link"])
                    db.session.add(new_song)
                    db.session.commit()

                new_song_location = song_locations(user_id=session["user_id"], track_id=current_track_info["id"], longitude=lng, latitude=lat, date=date, emotion=emotion, comment=comment, is_private=is_private)
                db.session.add(new_song_location)
                db.session.commit()     
            session['current_id'] = current_track_info['id']
            return redirect(url_for('profile', display_user_id=session['user_id']))

        except TypeError as e:
            print(
                # エラーの場合原因返す
                e
            )
            return redirect("/")

# 現在再生されている曲情報を取得
def get_current_track():
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    id = sp.current_playback()['item']['id']
    track_name = sp.current_playback()['item']['name']
    artists = [artist for artist in sp.current_playback()['item']['artists']]
    # artist_names = sp.current_playback()['item']['artists']['name']
    # link = sp.current_playback()['item']['album']['external_urls'] #こっちだとアルバムのURL
    link = sp.current_playback()['item']['external_urls']['spotify'] #こっちは曲単体のURL
    image = sp.current_playback()['item']['album']['images'][2]['url']
    # artistが複数ある場合に結合して一つの文字列にする
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

memory_data=[]
@app.route('/create_memory', methods = ['GET', 'POST'])
@login_required
def create_memory():
    googlemapURL = "https://maps.googleapis.com/maps/api/js?key="+GOOGLE_MAP_API_KEY
    if request.method == "POST":
        lat = request.form.get('lat')
        lng = request.form.get('lng')
        print(lat)
        print(lng)
        memory_data.append({'lat': lat, 'lng': lng})
        return render_template('create_memory.html', lat=lat, lng=lng)
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    return render_template('create_memory.html', lat=memory_data[0]['lat'], lng=memory_data[0]['lng'], GOOGLEMAPURL=googlemapURL, user_id=session["user_id"])


@app.route('/create_memory/emotion', methods = ['POST'])
@login_required
def create_memory_emotion():
    memory={}
    session['token_info'], authorized = get_token()
    session.modified = True
    if not authorized:
        return redirect('/spotify-login')    
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    try:
        current_track_info = get_current_track()
        # POSTの受け取り
        lat = request.form.get('lat')
        lng = request.form.get('lng')
        date = request.form.get('date')
        # get_current_track()で取得したIDを以前取得したものと比較して異なっていたら新しい曲とみなし書き込む。
        if current_track_info['id'] != session['current_id']:
            exist_song = db.session.query(songs).filter(songs.track_id == current_track_info["id"]).all()
            if exist_song == []:
                print(current_track_info["artists"])
                new_song = songs(track_id=current_track_info["id"], track_name=current_track_info["track_name"], artist_name=current_track_info["artists"], track_image=current_track_info["image"], spotify_url=current_track_info["link"])
                db.session.add(new_song)
                db.session.commit()
        else:
            # 同じ曲の時
            return redirect('/')
        memory['lat']=lat
        memory['lng']=lng
        memory['date']=date
        memory['track_id']=current_track_info['id']
        print(memory)
        session['current_id'] = current_track_info['id']
        return render_template('create_memory_emotion.html', memory=memory, user_id=session['user_id'])
    except TypeError as e:
        print(
            # エラーの場合原因返す
            e
        )
    return redirect("/")

@app.route('/create_memory/about', methods = ['POST'])
@login_required
def memory_about():
    memory={}
    lat = request.form.get('lat')
    lng = request.form.get('lng')
    date = request.form.get('date')
    track_id = request.form.get('track_id')
    emotion = request.form.get('emotion')

    memory['lat']=lat
    memory['lng']=lng
    memory['date']=date
    memory['track_id']=track_id
    memory['emotion']=emotion
    
    return render_template('create_memory_about.html', user_id=session["user_id"], memory = memory)


@app.route("/create_memory/confirm", methods=['POST'])
@login_required
def create_memory_confirm():
    googlemapURL = "https://maps.googleapis.com/maps/api/js?key="+GOOGLE_MAP_API_KEY
    memory={}
    lat = request.form.get('lat')
    lng = request.form.get('lng')
    date = request.form.get('date')
    track_id = request.form.get('track_id')
    emotion = request.form.get('emotion')
    about = request.form.get('about')

    memory['lat']=lat
    memory['lng']=lng
    memory['date']=date
    memory['track_id']=track_id
    memory['emotion']=emotion
    memory['about']=about

    print( memory) 
    return render_template('create_memory_confirm.html', memory=memory, user_id=session["user_id"],GOOGLEMAPURL=googlemapURL,lat=memory['lat'], lng=memory['lng'])

@app.route("/create_memory/complete", methods=['POST'])
@login_required
def create_memory_complete():
    lat = request.form.get('lat')
    lng = request.form.get('lng')
    date_str = request.form.get('date')
    Datetime = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    date = Datetime.date()
    track_id = request.form.get('track_id')
    emotion = request.form.get('emotion')
    about = request.form.get('about')
    comment = request.form.get('comment')
    pin_status = request.form.get('pin_status')
    is_private = ""
    if pin_status == "private":
        is_private = "True"
    elif pin_status == "public":
        is_private = "False"

    new_song_location = song_locations(user_id=session["user_id"], track_id=track_id, longitude=lng, latitude=lat, date=date, emotion=emotion, comment=comment,about=about, is_private=is_private)
    db.session.add(new_song_location)
    db.session.commit()
    return redirect("/create_memory")


@app.route('/map/<song_location_id>/edit', methods=['GET','POST'])
def edit_map(song_location_id):
    songdata = []
    googlemapURL = "https://maps.googleapis.com/maps/api/js?key="+GOOGLE_MAP_API_KEY
    song_location = db.session.query(song_locations).filter(song_locations.id == song_location_id).first()
    # song_locationがないか、他のユーザーのsong_locationの場合
    if not song_location or  song_location.user_id != session["user_id"]:
        return redirect('/')
    song = db.session.query(songs).filter(songs.track_id == song_location.track_id).first()
    songdata.append({'id':song_location.id,'user_id':song_location.user_id, 'lat':song_location.latitude, 'lng':song_location.longitude, 'date':song_location.date.strftime("%Y-%m-%d"),'artist':song.artist_name, 'track':song.track_name, 'image':song.track_image ,'link':song.spotify_url, 'emotion':song_location.emotion, 'comment':song_location.comment,'about':song_location.about, 'is_private':song_location.is_private})
    if request.method == "POST":
        if request.form.get('date'): 
            date_str = request.form.get('date')
            Datetime = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            date = Datetime.date()
            print(date)
            print("is registerd")
            # loadingで現在地追加の日付を使う場合
        else:
            date = datetime.date.today()
            # Datetime = datetime.datetime.now()
            print(date)
            print("is today")
        song_location.date = date
        song_location.emotion = request.form.get('emotion')
        song_location.comment = request.form.get('comment')
        song_location.about = request.form.get('about')
        pin_status = request.form.get('pin_status')
        is_private = ""
        if pin_status == "private":
            is_private = "True"
        elif pin_status == "public":
            is_private = "False"
        song_location.is_private = is_private
        db.session.commit()
        return redirect('/')
    else:
        return render_template('edit_map.html', GOOGLEMAPURL=googlemapURL, Songdatas=songdata, user_id=session["user_id"], lat=song_location.latitude, lng=song_location.longitude)

@app.route('/map/<song_location_id>/delete', methods=['GET'])
def deletePin(song_location_id):
    song_location = db.session.query(song_locations).filter(song_locations.id == song_location_id).first()
    # song_locationがないか、他のユーザーのsong_locationの場合
    if not song_location or song_location.user_id != session["user_id"]:
        return redirect('/')
    db.session.delete(song_location)
    db.session.commit()
    print("delete pin")
    return redirect(url_for('profile', display_user_id=session['user_id']))


# プロフィールで期間指定
@app.route('/profile/<display_user_id>/period/<displayfrom>/<displayto>', methods = ['GET','POST'])
def profilePeriod(display_user_id, displayfrom, displayto):
    session['token_info'], authorized = get_token()
    session.modified = True
    # していなかったらリダイレクト。
    if not authorized:
        return redirect('/spotify-login')    
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    # ユーザの情報
    login_user_id = session["user_id"]

    profile_info = Profile_info(login_user_id, display_user_id, "period", displayfrom, displayto, None, None, None, None, GOOGLE_MAP_API_KEY)
    user_info = profile_info["user_info"]
    googlemapURL = profile_info["googlemapURL"]
    songdata = profile_info["songdata"]
    latestsongdata = profile_info["latestsongdata"]

    # 自己紹介文取得
    if db.session.query(users.introduce).filter(users.id == session['user_id']).all()[0][0] != None:
        Introduce = db.session.query(users.introduce).filter(users.id == session['user_id']).all()[0][0]
    else:
        Introduce ="Settingで自己紹介入力してください"
    
    status = "period"

    if request.method == "GET":
        return render_template('profile.html',user_id=session["user_id"] ,user_info=user_info, GOOGLEMAPURL=googlemapURL ,Songdatas=songdata,  nowdisplayfrom=displayfrom, nowdisplayto=displayto, display_user_id=display_user_id, latestsongdata = latestsongdata, Introduce=Introduce, status = status)
    
    if request.method == "POST":
        #makeplaylistにデータ渡す
        playlist_name = request.form['playlistname']
        return render_template('makeplaylist.html', data = songdata, name = playlist_name, user_id=session["user_id"])
# プロフィールで期間指定

# プロフィールで感情指定
@app.route('/profile/<display_user_id>/emotion/<emotion>', methods = ['GET','POST'])
def profileEmotion(display_user_id,emotion):
    session['token_info'], authorized = get_token()
    session.modified = True
    # していなかったらリダイレクト。
    if not authorized:
        return redirect('/spotify-login')    
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    # ユーザの情報
    login_user_id = session["user_id"]

    profile_info = Profile_info(login_user_id, display_user_id, "emotion", None, None, emotion, None, None, None, GOOGLE_MAP_API_KEY)
    user_info = profile_info["user_info"]
    googlemapURL = profile_info["googlemapURL"]
    songdata = profile_info["songdata"]
    latestsongdata = profile_info["latestsongdata"]
    # 自己紹介文取得
    if db.session.query(users.introduce).filter(users.id == session['user_id']).all()[0][0] != None:
        Introduce = db.session.query(users.introduce).filter(users.id == session['user_id']).all()[0][0]
    else:
        Introduce ="Settingで自己紹介入力してください"

    status = "emotion"

    if request.method == "GET":
        return render_template('profile.html',user_id=session["user_id"] ,user_info=user_info, GOOGLEMAPURL=googlemapURL ,Songdatas=songdata, display_user_id=display_user_id, emotion = emotion, latestsongdata = latestsongdata, Introduce = Introduce, status = status)
    
    if request.method == "POST":
        #makeplaylistにデータ渡す
        playlist_name = request.form['playlistname']
        return render_template('makeplaylist.html', data = songdata, name = playlist_name, user_id=session["user_id"])

# プロフィールでジャンル指定
@app.route('/profile/<display_user_id>/about/<about>', methods = ['GET','POST'])
def profileAbout(display_user_id,about):
    session['token_info'], authorized = get_token()
    session.modified = True
    # していなかったらリダイレクト。
    if not authorized:
        return redirect('/spotify-login')    
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    # ユーザの情報
    login_user_id = session["user_id"]

    profile_info = Profile_info(login_user_id, display_user_id, "about", None, None, None, about, None, None, GOOGLE_MAP_API_KEY)
    user_info = profile_info["user_info"]
    googlemapURL = profile_info["googlemapURL"]
    songdata = profile_info["songdata"]
    latestsongdata = profile_info["latestsongdata"]
    # 自己紹介文取得
    if db.session.query(users.introduce).filter(users.id == session['user_id']).all()[0][0] != None:
        Introduce = db.session.query(users.introduce).filter(users.id == session['user_id']).all()[0][0]
    else:
        Introduce ="Settingで自己紹介入力してください"

    status = "emotion"

    if request.method == "GET":
        return render_template('profile.html',user_id=session["user_id"] ,user_info=user_info, GOOGLEMAPURL=googlemapURL ,Songdatas=songdata, display_user_id=display_user_id, about = about, latestsongdata = latestsongdata, Introduce = Introduce, status = status)
    
    if request.method == "POST":
        #makeplaylistにデータ渡す
        playlist_name = request.form['playlistname']
        return render_template('makeplaylist.html', data = songdata, name = playlist_name, user_id=session["user_id"])


# プロフィールでアーティスト指定
@app.route('/profile/<display_user_id>/artist/<artist>', methods = ['GET','POST'])
def profileArtist(display_user_id,artist):
    session['token_info'], authorized = get_token()
    session.modified = True
    # していなかったらリダイレクト。
    if not authorized:
        return redirect('/spotify-login')    
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    # ユーザの情報
    login_user_id = session["user_id"]

    profile_info = Profile_info(login_user_id, display_user_id, "artist", None, None, None, None, artist, None, GOOGLE_MAP_API_KEY)
    user_info = profile_info["user_info"]
    googlemapURL = profile_info["googlemapURL"]
    songdata = profile_info["songdata"]
    latestsongdata = profile_info["latestsongdata"]
    # 自己紹介文取得
    if db.session.query(users.introduce).filter(users.id == session['user_id']).all()[0][0] != None:
        Introduce = db.session.query(users.introduce).filter(users.id == session['user_id']).all()[0][0]
    else:
        Introduce ="Settingで自己紹介入力してください"

    status = "artist_name"

    if request.method == "GET":
        return render_template('profile.html',user_id=session["user_id"] ,user_info=user_info, GOOGLEMAPURL=googlemapURL ,Songdatas=songdata, display_user_id=display_user_id, artist=artist , latestsongdata = latestsongdata, Introduce = Introduce, status = status)
    
    if request.method == "POST":
        #makeplaylistにデータ渡す
        playlist_name = request.form['playlistname']
        return render_template('makeplaylist.html', data = songdata, name = playlist_name, user_id=session["user_id"], status = status)

# プロフィールで曲指定
@app.route('/profile/<display_user_id>/song_name/<song_name>', methods = ['GET','POST'])
def profileSong(display_user_id, song_name):
    session['token_info'], authorized = get_token()
    session.modified = True
    # していなかったらリダイレクト。
    if not authorized:
        return redirect('/spotify-login')    
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    # ユーザの情報
    login_user_id = session["user_id"]

    profile_info = Profile_info(login_user_id, display_user_id, "song_name", None, None, None, None, None, song_name, GOOGLE_MAP_API_KEY)
    user_info = profile_info["user_info"]
    googlemapURL = profile_info["googlemapURL"]
    songdata = profile_info["songdata"]
    latestsongdata = profile_info["latestsongdata"]

    # 自己紹介文取得
    if db.session.query(users.introduce).filter(users.id == session['user_id']).all()[0][0] != None:
        Introduce = db.session.query(users.introduce).filter(users.id == session['user_id']).all()[0][0]
    else:
        Introduce ="Settingで自己紹介入力してください"

    status = "track_name"

    if request.method == "GET":
        return render_template('profile.html',user_id=session["user_id"] ,user_info=user_info, GOOGLEMAPURL=googlemapURL ,Songdatas=songdata, display_user_id=display_user_id ,song_name=song_name, latestsongdata = latestsongdata, Introduce = Introduce, status = status)
    
    if request.method == "POST":
        #makeplaylistにデータ渡す
        playlist_name = request.form['playlistname']
        return render_template('makeplaylist.html', data = songdata, name = playlist_name, user_id=session["user_id"])
# プロフィールで曲指定


@app.route('/makeplaylist', methods=['GET','POST'])
def makeplaylist():
    session['token_info'], authorized = get_token()
    session.modified = True
    # していなかったらリダイレクト。
    if not authorized:
        return redirect('/spotify-login')
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))

    if request.method == 'POST':

        url_list = request.form.getlist('urls')
        # flash("以下の曲が条件に当てはまりました", "success")
        playlist_name = request.form.get("playlist_name")
        sp_user_id = sp.current_user()['id']
        
        new_playlist = sp.user_playlist_create(sp_user_id, playlist_name)
        sp.user_playlist_add_tracks(sp_user_id, new_playlist["id"], url_list)

        #プレイリストIDをsessionに保存
        playlist_id = sp.current_user_playlists()['items'][0]['id']
        #プレイリストURIをsessionに保存
        playlist_uri_test = sp.current_user_playlists()['items'][0]['uri']
        # playlist_uri = playlist_uri_test.removeprefix('spotify:playlist:')
        playlist_uri = playlist_uri_test.replace('spotify:playlist:', '')
        session['playlist_uri'] = playlist_uri

        playlist_image = sp.playlist_cover_image(playlist_id)[0]['url']
        playlist_name =sp.playlist(playlist_id)["name"]

        new_playlist = made_playlists(user_id=session["user_id"],playlist_id = playlist_id ,playlist_uri=playlist_uri,playlist_image=playlist_image,playlist_name=playlist_name)
        db.session.add(new_playlist)
        db.session.commit()    
        
        playlistaa = db.session.query(made_playlists.playlist_uri).filter(made_playlists.user_id == session["user_id"]).all()
        # print("play",playlistaa[0] )

        return redirect(url_for('playlist', display_user_id=session['user_id']))


@app.route('/profile/<display_user_id>/playlist/', methods = ['GET'])
def playlist(display_user_id):
    session['token_info'], authorized = get_token()
    session.modified = True
    # していなかったらリダイレクト。
    if not authorized:
        return redirect('/spotify-login')    
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))

    
    playlist_date = db.session.query(made_playlists).filter(made_playlists.user_id == display_user_id).all()
    playlists =[]

    for pin in playlist_date:
        # print(sp.playlist(pin.playlist_id)["name"])
        playlists.append({'id':pin.id,'user_id':pin.user_id, 'playlist_id':pin.playlist_id, 'playlist_uri':pin.playlist_uri,
        'playlist_image':pin.playlist_image,'playlist_name':pin.playlist_name})
    display_user = db.session.query(users.nickname).filter(users.id == display_user_id).first()
    display_user_id = db.session.query(users.id).filter(users.id == display_user_id).first()[0]
   
    return render_template('playlist.html', playlists = playlists,user_id = session['user_id'], display_user = display_user, display_user_id=display_user_id) 

@app.route('/delete_playlist/', methods = ['POST'])
def deletePlaylist():
    if request.method == 'POST':
        session['token_info'], authorized = get_token()
        session.modified = True
        # していなかったらリダイレクト。
        if not authorized:
            return redirect('/spotify-login')    
        sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
        
        deletelists = request.form.getlist("deletelists")
        for i in deletelists:
            sp.current_user_unfollow_playlist(i)
            deleting = db.session.query(made_playlists).filter(made_playlists.user_id == session['user_id'] , made_playlists.playlist_id == i).first()
            db.session.delete(deleting)
            db.session.commit()
        
        return redirect(url_for('playlist', display_user_id=session['user_id']))


@app.route('/add_playlist/', methods = ['POST'])
def addPlaylist():
    if request.method == 'POST':
        session['token_info'], authorized = get_token()
        session.modified = True
        # していなかったらリダイレクト。
        if not authorized:
            return redirect('/spotify-login')    
        sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
        
        addlists = request.form.getlist("deletelists")
        for i in addlists:
            sp.current_user_follow_playlist(i)

        #プレイリストIDをsessionに保存
            playlist_id = sp.current_user_playlists()['items'][0]['id']
            #プレイリストURIをsessionに保存
            playlist_uri_test = sp.current_user_playlists()['items'][0]['uri']
            # playlist_uri = playlist_uri_test.removeprefix('spotify:playlist:')
            playlist_uri = playlist_uri_test.replace('spotify:playlist:', '')
            session['playlist_uri'] = playlist_uri

            playlist_image = sp.playlist_cover_image(playlist_id)[0]['url']
            playlist_name =sp.playlist(playlist_id)["name"]

            new_playlist = made_playlists(user_id=session["user_id"],playlist_id = playlist_id ,playlist_uri=playlist_uri,playlist_image=playlist_image,playlist_name=playlist_name)
            db.session.add(new_playlist)
            db.session.commit()  
        
        return redirect(url_for('playlist', display_user_id=session['user_id']))

@app.route('/songlocations/<songlocation_id>', methods=['GET'])
def show_song_location(songlocation_id):
    googlemapURL = "https://maps.googleapis.com/maps/api/js?key="+GOOGLE_MAP_API_KEY
    songlocation = db.session.query(song_locations).filter(song_locations.id == songlocation_id).first()
    login_user = db.session.query(users).filter(users.id == session["user_id"]).first()
    print(songlocation.latitude,songlocation.longitude)
    song = db.session.query(songs).filter(songs.track_id == songlocation.track_id).first()

    songdata = {'id':songlocation.id,'lat':songlocation.latitude, 'lng':songlocation.longitude, 'date':songlocation.date.strftime("%Y-%m-%d"),'artist':song.artist_name, 'track':song.track_name, 'image':song.track_image ,'link':song.spotify_url, 'user_id':songlocation.user_id, 'emotion':songlocation.emotion, 'comment':songlocation.comment, 'is_private':songlocation.is_private, 'track_id':songlocation.track_id, 'about':songlocation.about, 'user_nickname':login_user.nickname, 'image':song.track_image}
    return render_template("show_songlocation.html", songdata=songdata, lat=songlocation.latitude, lng=songlocation.longitude,GOOGLEMAPURL=googlemapURL, user_id=session["user_id"] )


# HOMEで時期指定
@app.route('/home/period/<displayfrom>/<displayto>', methods = ['GET'])
def homePeriod(displayfrom, displayto):
    session['token_info'], authorized = get_token()
    session.modified = True
    # していなかったらリダイレクト。
    if not authorized:
        return redirect('/spotify-login')    
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))

    # ユーザの情報
    login_user_id = session["user_id"]

    profile_info = Home_info(login_user_id, "period", displayfrom, displayto, None, None, None, None, GOOGLE_MAP_API_KEY)
    user_info = profile_info["user_info"]
    googlemapURL = profile_info["googlemapURL"]
    songdata = profile_info["songdata"]
    latestsongdata = profile_info["latestsongdata"]

        #最新3件の投稿をリスト表示させる

    status = "period"

    return render_template('index.html',user_id=session["user_id"] ,user_info=user_info, GOOGLEMAPURL=googlemapURL ,Songdatas=songdata, nowdisplayfrom=displayfrom, nowdisplayto=displayto, latestsongdata=latestsongdata, status = status)

# ホームで感情指定
@app.route('/home/emotion/<emotion>', methods = ['GET'])
def homeEmotion(emotion):
    session['token_info'], authorized = get_token()
    session.modified = True
    # していなかったらリダイレクト。
    if not authorized:
        return redirect('/spotify-login')    
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    # ユーザの情報
    login_user_id = session["user_id"]

    profile_info = Home_info(login_user_id, "emotion", None, None, emotion, None, None, None, GOOGLE_MAP_API_KEY)
    user_info = profile_info["user_info"]
    googlemapURL = profile_info["googlemapURL"]
    songdata = profile_info["songdata"]
    latestsongdata = profile_info["latestsongdata"]
    print(latestsongdata)

    status= "emotion"

    return render_template('index.html',user_id=session["user_id"] ,user_info=user_info, GOOGLEMAPURL=googlemapURL ,Songdatas=songdata,latestsongdata=latestsongdata, status=status, emotion=emotion)
# ホームで感情指定

# ホームでジャンル指定
@app.route('/home/about/<about>', methods = ['GET'])
def homeAbout(about):
    if about == "":
        return redirect("/")
    session['token_info'], authorized = get_token()
    session.modified = True
    # していなかったらリダイレクト。
    if not authorized:
        return redirect('/spotify-login')    
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    # ユーザの情報
    login_user_id = session["user_id"]

    profile_info = Home_info(login_user_id, "about", None, None, None, about, None, None, GOOGLE_MAP_API_KEY)
    user_info = profile_info["user_info"]
    googlemapURL = profile_info["googlemapURL"]
    songdata = profile_info["songdata"]
    latestsongdata = profile_info["latestsongdata"]
    print(latestsongdata)

    status= "about"

    print(songdata)

    return render_template('index.html',user_id=session["user_id"] ,user_info=user_info, GOOGLEMAPURL=googlemapURL ,Songdatas=songdata,latestsongdata=latestsongdata, status=status, about=about)
# ホームで感情指定

# ホームでアーティスト指定
@app.route('/home/artist/<artist>', methods = ['GET'])
def homeArtist(artist):
    session['token_info'], authorized = get_token()
    session.modified = True
    # していなかったらリダイレクト。
    if not authorized:
        return redirect('/spotify-login')    
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    # ユーザの情報
    login_user_id = session["user_id"]

    profile_info = Home_info(login_user_id, "artist", None, None, None, None, artist, None, GOOGLE_MAP_API_KEY)
    user_info = profile_info["user_info"]
    googlemapURL = profile_info["googlemapURL"]
    songdata = profile_info["songdata"]
    latestsongdata = profile_info["latestsongdata"]

    status="artist_name"

    return render_template('index.html',user_id=session["user_id"] ,user_info=user_info, GOOGLEMAPURL=googlemapURL ,Songdatas=songdata,latestsongdata=latestsongdata, status=status, artist=artist)
# ホームでアーティスト指定

# ホームで曲指定
@app.route('/home/song_name/<song_name>', methods = ['GET'])
def homeSong(song_name):
    session['token_info'], authorized = get_token()
    session.modified = True
    # していなかったらリダイレクト。
    if not authorized:
        return redirect('/spotify-login')    
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    # ユーザの情報
    login_user_id = session["user_id"]

    profile_info = Home_info(login_user_id, "song_name", None, None, None, None, None, song_name, GOOGLE_MAP_API_KEY)
    user_info = profile_info["user_info"]
    googlemapURL = profile_info["googlemapURL"]
    songdata = profile_info["songdata"]
    latestsongdata = profile_info["latestsongdata"]

    status="song_name"

    return render_template('index.html',user_id=session["user_id"] ,user_info=user_info, GOOGLEMAPURL=googlemapURL ,Songdatas=songdata,latestsongdata=latestsongdata, status = status, song_name=song_name)
# ホームでアーティスト曲指定

@app.route('/select_location', methods = ['GET'])
@login_required
def select_location():
    session['token_info'], authorized = get_token()
    session.modified = True
    # していなかったらリダイレクト。
    if not authorized:
        return redirect('/spotify-login')
    songdata = []
    pins = db.session.query(song_locations).filter(song_locations.user_id == session["user_id"]).all()
    for pin in pins:
        song = db.session.query(songs).filter(songs.track_id == pin.track_id).first()
        songdata.append({'id':pin.id,'lat':pin.latitude, 'lng':pin.longitude, 'date':pin.date.strftime("%Y-%m-%d"),
        'artist':song.artist_name, 'track':song.track_name, 'image':song.track_image ,'link':song.spotify_url, 'user_id':pin.user_id, 'emotion':pin.emotion, 'comment':pin.comment, 'is_private':pin.is_private})
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    googlemapURL = "https://maps.googleapis.com/maps/api/js?key="+GOOGLE_MAP_API_KEY   
    return render_template('select_location.html', GOOGLEMAPURL=googlemapURL, Songdatas = songdata, user_id = session["user_id"])



@app.route('/profile/<display_user_id>/follower', methods = ['GET'])
@login_required
def display_follower(display_user_id):
    user = db.session.query(users).filter(users.id == display_user_id).first()
    user_info = dict(id=user.id, nickname=user.nickname, username=user.username)
    followings = db.session.query(follow).filter(follow.follow_user_id == display_user_id).all()
    followeds = db.session.query(follow).filter(follow.followed_user_id == display_user_id).all()

    following_user_info = []
    for following in followings:
        other_user = db.session.query(users).filter(users.id == following.followed_user_id).first()
        other_user_info = dict(id=other_user.id, nickname=other_user.nickname, username=other_user.username)
        following_user_info.append(other_user_info)

    followed_user_info = []
    for followed in followeds:
        other_user = db.session.query(users).filter(users.id == followed.follow_user_id).first()
        other_user_info = dict(id=other_user.id, nickname=other_user.nickname, username=other_user.username)
        followed_user_info.append(other_user_info)
    
    return render_template("follower.html",user_id=session["user_id"], user_info=user_info, following_user_info=following_user_info, followed_user_info=followed_user_info)


@app.route('/groups', methods = ['GET', 'POST'])
@login_required
def groups():
    login_user_id=session["user_id"]
    if request.method == "POST":
        # 許可するかどうか、owner_id, group_idを受け取る。
        auth = request.form.get("auth")
        owner_id = request.form.get("owner_id")
        group_id = request.form.get("group_id")
        print("auth",auth, "owner", owner_id, "group", group_id)
# ここのowneridがタプルになる

        # auth = "yes"
        if auth == "yes":
            new_user_group = UserGroup(group_id = group_id, owner_id = owner_id, invited_id = login_user_id)
            db.session.add(new_user_group)
            db.session.commit()
# リクエストを消す
        # delete_request = db.session.query(requests).filter(requests.group_id == group_id).filter(requests.owner_id == owner_id,).filter(requests.invited_id == login_user_id).first()
        delete_request = db.session.query(requests).filter(requests.group_id == group_id).first()
        print("delete",delete_request)
        db.session.delete(delete_request)
        db.session.commit()
        
    user = db.session.query(users).filter(users.id == login_user_id).first()
    user_info = dict(id=user.id, nickname=user.nickname, username=user.username)

    # owner_group_ids = db.session.query(UserGroup.group_id).filter(UserGroup.owner_id == login_user_id).all()
    owner_group_ids = db.session.query(Group.id).filter(Group.owner_id == login_user_id).all()
    invited_group_ids = db.session.query(UserGroup.group_id).filter(UserGroup.invited_id == login_user_id).all()
    requests_group_ids = db.session.query(requests.group_id).filter(requests.invited_id == login_user_id).all()
    requests_owner_group_ids = db.session.query(requests.group_id).filter(requests.owner_id == login_user_id).all()
    print("owner", owner_group_ids)
    groups = []
    requests_groups = []
#グループ一覧（自分が作ったやつ） 
    for owner_group_id in owner_group_ids:
        owner_group = db.session.query(Group).filter(Group.id == owner_group_id[0]).first()
        # print('Oid',owner_group.id,'Oname',owner_group.name)
        groups.append(dict(id=owner_group.id, name=owner_group.name, owner_id=owner_group.owner_id))
#グループ一覧（自分が招待されて参加済みのやつ） 
    for invited_group_id in invited_group_ids:
        invited_group = db.session.query(Group).filter(Group.id == invited_group_id[0]).first()
        # print('Iid',invited_group.id)
        if invited_group:
            groups.append(dict(id=invited_group.id, name=invited_group.name, owner_id=invited_group.owner_id))
        # groups.append(dict(id=user_info.id, username=user_info.username, nickname=user_info.nickname, track_id=track_id))

# グループ一覧（自分が作ってまだ参加してない人いてrequestテーブルにあるやつ）
    # for requests_group_id in requests_owner_group_ids:
    #     requests_group = db.session.query(Group).filter(Group.id == requests_group_id[0]).first()
    #     # requests_group_owner = db.session.query(UserGroup.owner_id).filter(UserGroup.group_id == requests_group_id[0]).first()
    #     # print('Rid',requests_group.id)
    #     groups.append(dict(id=requests_group.id, name=requests_group.name))
# 招待一覧
    for requests_group_id in requests_group_ids:
        requests_group = db.session.query(Group).filter(Group.id == requests_group_id[0]).first()
        # requests_group_owner = db.session.query(Group.owner_id).filter(UserGroup.id == requests_group_id[0]).first()
        print('一覧ownerid',requests_group.owner_id)

        requests_groups.append(dict(id=requests_group.id, name=requests_group.name, owner_id=requests_group.owner_id))

    return render_template("groups.html", user_id=session["user_id"], user_info=user_info, groups=groups, requests_groups=requests_groups)


@app.route('/create_group', methods = ['GET'])
@login_required
def create_group():
    login_user_id=session["user_id"]
    user = db.session.query(users).filter(users.id == login_user_id).first()
    user_info = dict(id=user.id, nickname=user.nickname, username=user.username)
    followings = db.session.query(follow).filter(follow.follow_user_id == login_user_id).all()

    following_user_info = []
    for following in followings:
        other_user = db.session.query(users).filter(users.id == following.followed_user_id).first()
        other_user_info = dict(id=other_user.id, nickname=other_user.nickname, username=other_user.username)
        following_user_info.append(other_user_info)
    
    return render_template("create_group.html", user_id=session["user_id"], user_info=user_info, following_user_info=following_user_info)

@app.route('/create_group_table', methods = ['POST'])
@login_required
# profile->follow->home
def create_group_table():
    login_user_id = session["user_id"]
    group_name = request.form.get("group_name")
    add_user_ids = request.form.getlist("add_users")
    print("add_user_id", add_user_ids)

    new_group = Group(owner_id=login_user_id, name = group_name, introduction = "")
    db.session.add(new_group)
    db.session.commit()

    new_group_id = db.session.query(func.max(Group.id).label('max'))
    print("newgroup")
    print(new_group_id[0]['max'])

    for add_user_id in add_user_ids:
        new_user_group = requests(group_id = new_group_id[0]['max'], owner_id = login_user_id, invited_id = add_user_id)
        db.session.add(new_user_group)
        db.session.commit()
        print("group_id = ", new_group_id[0]['max'], "owner_id = ", login_user_id, "invited_id = ", add_user_id)
    
    # 作ったグループ確認
    rows = db.session.query(requests).all()
    for row in rows:
        print("Groupid",row.group_id)
        print("Groupuser",row.owner_id, end="->")
        print("Groupinvited",row.invited_id)
    
    return redirect("/groups")

@app.route('/groups/<group_id>', methods = ['GET'])
@login_required
def group_info(group_id):
    # グループの情報
    group = db.session.query(Group).filter(Group.id == group_id).first()
    group_info = dict(id=group.id, name=group.name, introduction=group.introduction )

    tracks =[]
    track_lists=[]

    try: #招待メンバー一人でも参加済みのとき
        group_members = db.session.query(UserGroup.invited_id).filter(UserGroup.group_id == group_id).all()
        group_owner = db.session.query(Group.owner_id).filter(Group.id == group_id).all()[0][0]
        owner_pins = db.session.query(song_locations).filter(song_locations.user_id == group_owner).all()
        random_num = random.randint(0,len(owner_pins)-1)
        # print("rando",random_num,"len",len(owner_pins)-1)
        tracks.append(owner_pins[random_num])
        # for pin in owner_pins:
        #     tracks.append(pin)
            
        for group_member in group_members:
            print("member",group_member.invited_id)
            user_pins = db.session.query(song_locations).filter(song_locations.user_id == group_member.invited_id).all()
            random_num = random.randint(0,len(user_pins)-1)
            print("rando",random_num,"len",len(user_pins)-1)
            tracks.append(user_pins[random_num])
            # for pin in user_pins:
            #     tracks.append(pin)
                
    except:#まだ招待メンバー一人も参加していないとき
        group_owner = db.session.query(Group.owner_id).filter(Group.id == group_id).all()[0][0]
    
        owner_pins = db.session.query(song_locations).filter(song_locations.user_id == group_owner).all()
        random_num = random.randint(0,len(owner_pins)-1)
        # print("rando",random_num,"len",len(owner_pins)-1)
        tracks.append(owner_pins[random_num])
        # for pin in owner_pins:
        #     tracks.append(pin)
    #try,exept 共通処理 
    for track in tracks:
            # print(pin)
            song = db.session.query(songs).filter(songs.track_id == track.track_id).first()
            user = db.session.query(users).filter(users.id == track.user_id).first()
            # ログインユーザがいいねしてあるか判定
            print('pinnnnnn',track.id)
            # db.session.query(likes.song_location_id).filter(likes.user_id == session['user_id']).filter(likes.song_location_id == track.id).all()[0] == track.id
            # for i in likelist:
            #     print("kore",i[0])
            # print(db.session.query(exists().where(likes.song_location_id == track.id)).scalar())
            if db.session.query(exists().where(likes.song_location_id == track.id).where(likes.user_id == session['user_id'])).scalar() == True:
                print("True")
                track_lists.append({'like':'yes','id':track.id,'lat':track.latitude, 'lng':track.longitude, 'date':track.date.strftime("%Y-%m-%d"),
                'artist':song.artist_name, 'track':song.track_name, 'image':song.track_image ,'link':song.spotify_url, 'track_id':song.track_id, 'user_id':track.user_id, 'emotion':track.emotion, 'about':track.about, 'comment':track.comment, 'is_private':track.is_private, 'user_nickname':user.nickname})
            else:
                track_lists.append({'like':'no','id':track.id,'lat':track.latitude, 'lng':track.longitude, 'date':track.date.strftime("%Y-%m-%d"),
                'artist':song.artist_name, 'track':song.track_name, 'image':song.track_image ,'link':song.spotify_url, 'track_id':song.track_id, 'user_id':track.user_id, 'emotion':track.emotion, 'about':track.about, 'comment':track.comment, 'is_private':track.is_private, 'user_nickname':user.nickname})

    return render_template("group_info.html",user_id=session['user_id'], group_info=group_info, track_lists=track_lists)


@app.route('/groups/<group_id>/members', methods = ['GET'])
@login_required
def group_members(group_id):
    group = db.session.query(Group).filter(Group.id == group_id).first()
    group_info = dict(owner_id = group.owner_id,id=group.id, name=group.name, introduction=group.introduction)

    group_members = db.session.query(UserGroup).filter(UserGroup.group_id == group_id).all()
    group_members_info = []

#オーナ情報取り出し 
    owner_user_info = db.session.query(users).filter(users.id == group.owner_id).first()
    group_members_info.append(dict(id=owner_user_info.id, username=owner_user_info.username, nickname=owner_user_info.nickname))
# メンバー情報取り出し
    for group_member in group_members:
        print("i",group_member.invited_id,"o",group_member.owner_id)
        user_info = db.session.query(users).filter(users.id == group_member.invited_id).first()
        if user_info:
            group_members_info.append(dict(id=user_info.id, username=user_info.username, nickname=user_info.nickname))
# 招待中メンバー取り出し
    requesting_members  = db.session.query(requests).filter(requests.group_id == group_id).all()
    requesting_members_info = []
    for requesting_member in requesting_members:
        print("i",requesting_member.invited_id,"o",requesting_member.owner_id)
        user_info = db.session.query(users).filter(users.id == requesting_member.invited_id).first()
        if user_info:
            requesting_members_info.append(dict(id=user_info.id, username=user_info.username, nickname=user_info.nickname))
    
#新たに追加するために、メンバーではなく、招待中でもない、フォロー取り出し 
    login_user_id=session["user_id"]
    user = db.session.query(users).filter(users.id == login_user_id).first()
    user_info = dict(id=user.id, nickname=user.nickname, username=user.username)
    followings = db.session.query(follow).filter(follow.follow_user_id == login_user_id).all()
    following_user_info = []
    #全てのフォロー取得 
    for following in followings:
        other_user = db.session.query(users).filter(users.id == following.followed_user_id).first()
        print('user',other_user.id)
        other_user_info = dict(id=other_user.id, nickname=other_user.nickname, username=other_user.username)
        following_user_info.append(other_user_info)
    # メンバーと一致するもの削除
    for k in following_user_info:
        if k:
            for group_member in group_members_info:
                if k:
                    print("member",group_member['id'] ,"k",k['id'])
                    if k['id'] == group_member['id']:
                        k.clear()  #空で返すことになるからjinjaでif文つけてる
        
    # 招待と一致するもの削除 
    for k in following_user_info:
        if k: #上で空にした行の時にエラーになる
            print('followid',k['id'])
            for requesting_member in requesting_members_info:
                if requesting_member:
                    try:
                        if k:
                            print("request",requesting_member['id'] ,"k",k['id'])
                            if k['id'] == requesting_member['id']:
                                try:  
                                    k.clear() #空で返すことになるからjinjaでif文つけてる
                                except TypeError as e:
                                    print(e)
                    except TypeError as e:
                        print(e)
    for k in following_user_info:
        # 追加できるユーザーが一人でも残っていたらrenderに入れて渡す
        if k:
            print('finaluser',k["id"])
            return render_template("group_members.html", group_info=group_info, group_members_info=group_members_info,user_id=session['user_id'], requesting_members_info=requesting_members_info,following_user_info=following_user_info)
        else:
            print('残り無し')
    return render_template("group_members.html", group_info=group_info, group_members_info=group_members_info,user_id=session['user_id'], requesting_members_info=requesting_members_info)

@app.route('/add_group_user', methods = ['POST'])
@login_required
def add_member_table():
    add_user_ids = request.form.getlist("add_users")
    group_id = request.form.get("group_id")
    owner_id = request.form.get("owner_id")

    for add_user_id in add_user_ids:
        new_user_group = requests(group_id = group_id, owner_id = owner_id, invited_id = add_user_id)
        db.session.add(new_user_group)
        db.session.commit()

    return redirect(url_for('group_members', group_id=group_id))

@app.route('/notification', methods = ['GET'])
@login_required
def notification():
    login_user_id = session["user_id"]
    user = db.session.query(users).filter(users.id == login_user_id).first()
    user_info = dict(id=user.id, nickname=user.nickname, username=user.username)

    # 全てのピン取得
    pins = db.session.query(song_locations).filter(song_locations.user_id==login_user_id).all()
    pin_ids = []
    for pin in pins:
        # print(pin.id)
        pin_ids.append(pin.id)
    print(pin_ids)
    likelist = []
    for pin_id in pin_ids:
        likelist.extend(db.session.query(likes).filter(likes.song_location_id == pin_id).all())
    # sortしたい
    like_list = []
    for like in likelist:
        other_user = db.session.query(users).filter(users.id == like.user_id).first()
        like_list.append(dict(user_id = like.user_id, nickname=other_user.nickname, song_location_id = like.song_location_id, datetime = like.datetime))
        # print("songsssss")
        # print(like.song_location_id)

    followings= db.session.query(follow).filter(follow.followed_user_id == login_user_id).all()
    following_user_info = []
    for following in followings:
        other_user = db.session.query(users).filter(users.id == following.follow_user_id).first()
        other_user_info = dict(id=other_user.id, nickname=other_user.nickname, username=other_user.username)
        following_user_info.append(other_user_info)
    
    print(user_info, following_user_info, like_list)
    
    return render_template("notification.html",user_id=session["user_id"], user_info=user_info, following_user_info=following_user_info, like_list = like_list)
    

@app.route('/like', methods = ["POST"])
@login_required
def like():
    operator = session["user_id"]
    operated = request.form.get("user_id")
    song_location_id = request.form.get("song_location_id")
    like_or_cancell = request.form.get("like_or_cancell")
    if operator != operated:
        if like_or_cancell == "like":
            new_like = likes(user_id=operator, song_location_id=song_location_id, datetime=datetime.datetime.now())
            db.session.add(new_like)
            db.session.commit()
            print("like", end=": ")
            print(operated)
            rows = db.session.query(likes).all()
            for row in rows:
                print(row.user_id, end="->")
                print(row.song_location_id)
        elif like_or_cancell == "cancell":
            # 指定したデータを削除
            delete_likes = db.session.query(likes).filter_by(user_id=operator, song_location_id=song_location_id).all()
            print(delete_likes)
            for delete_like in delete_likes:
                db.session.delete(delete_like)
            db.session.commit()
            print("cancell", end=": ")
            print(operated)
            rows = db.session.query(likes).all()
            for row in rows:
                print(row.user_id, end="->")
                print(row.song_location_id)
        else:
            print("like error")
            return redirect("/")
        
        return redirect("/")

    return redirect("/")

## グループ名編集用、URL打ち込んで実行
# @app.route('/python_edit', methods = ['GET'])
# def python_edit():
## 編集したいグループID
#     group_id = 3 
#     group = db.session.query(Group).filter(Group.id == group_id).first()
##新しいグループ名
#     group.name="カナダ留学"
#     db.session.commit()
#     return redirect("/")

@app.route('/python_edit', methods = ['GET'])
def python_edit():
    group_id = 4
    group = db.session.query(Group).filter(Group.id == group_id).first()
    group.name="4番目のグループ名"
    db.session.commit()
    return redirect("/")

# if __name__ == '__main__':
#     app.run(host=os.getenv('APP_ADDRESS', 'localhost'), port=5000)
    
    
# if not app.debug or os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    # app.run(host=os.getenv('APP_ADDRESS', 'localhost'), port=5000)
    # app()
    # The app is not in debug mode or we are in the reloaded process

# if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
#     app.run(host=os.getenv('APP_ADDRESS', 'localhost'), port=5000)

    # app.run_server(use_reloader=False)

if __name__ == '__main__':
    # app.run(host=os.getenv('APP_ADDRESS', 'localhost'), port=5000)
    app()