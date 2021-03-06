from models import users, song_locations, songs, follow, made_playlists, likes, db
from sqlalchemy import or_, desc
from sqlalchemy.sql import exists

def Home_info(login_user_id, status, displayfrom, displayto, emotion, about, artist, song_name, GOOGLE_MAP_API_KEY):
    # フォローフォロワー数
    follow_user = db.session.query(follow).filter(follow.follow_user_id == login_user_id).all()
    if follow_user:
        follow_number = len(follow_user)
    else: 
        follow_number = 0

    followed_user = db.session.query(follow).filter(follow.followed_user_id == login_user_id).all()
    if followed_user:
        followed_number = len(followed_user)
    else:
        followed_number = 0
    nickname = db.session.query(users.nickname).filter(users.id == login_user_id).first()
    username = db.session.query(users.username).filter(users.id == login_user_id).first()
    user_info = dict(id=login_user_id, username=username[0], follow_number=follow_number, followed_number=followed_number, nickname=nickname[0])
    print(user_info)
    print(nickname)

    pins = []
    songdata = []
    latestpins = []
    latestsongdata = []
    googlemapURL = "https://maps.googleapis.com/maps/api/js?key="+GOOGLE_MAP_API_KEY

    
    if status == "emotion":
        # 地図用
        pins.extend(db.session.query(song_locations).filter(song_locations.user_id == login_user_id).filter(song_locations.emotion == emotion).all())
        for user in follow_user:
            pins.extend(db.session.query(song_locations).filter(song_locations.user_id == user.followed_user_id).filter(song_locations.emotion == emotion).filter(song_locations.is_private == "False").all())

        #リスト用 
        for f_user in follow_user:
            latestpins.extend(db.session.query(song_locations).filter(song_locations.user_id == f_user.followed_user_id).filter(song_locations.emotion == emotion).order_by(desc(song_locations.id)).limit(3).all())
        # for follow_pin in latestfollow_pins:
        #     latestpins.append(follow_pin)
            # latestfollow_pins = db.session.query(song_locations).filter(song_locations.user_id == f_user.followed_user_id).filter(song_locations.emotion == emotion).order_by(desc(song_locations.id)).limit(3).all()
        # for follow_pin in latestfollow_pins:
        #     latestpins.append(follow_pin)
    
    if status == "about":
        # 地図用
        pins.extend(db.session.query(song_locations).filter(song_locations.user_id == login_user_id).filter(song_locations.about == about).all())
        for user in follow_user:
            pins.extend(db.session.query(song_locations).filter(song_locations.user_id == user.followed_user_id).filter(song_locations.about == about).filter(song_locations.is_private == "False").all())

        #リスト用 
        for f_user in follow_user:
            latestpins.extend(db.session.query(song_locations).filter(song_locations.user_id == f_user.followed_user_id).filter(song_locations.about == about).order_by(desc(song_locations.id)).limit(3).all())
        # for follow_pin in latestfollow_pins:
        #     latestpins.append(follow_pin)
            # latestfollow_pins = db.session.query(song_locations).filter(song_locations.user_id == f_user.followed_user_id).filter(song_locations.emotion == emotion).order_by(desc(song_locations.id)).limit(3).all()
        # for follow_pin in latestfollow_pins:
        #     latestpins.append(follow_pin)


    if status == "period":
        pins.extend(db.session.query(song_locations).filter(song_locations.user_id == login_user_id).filter(song_locations.date >= displayfrom).filter(song_locations.date <= displayto).all())
        for user in follow_user:
            pins.extend(db.session.query(song_locations).filter(song_locations.user_id == user.followed_user_id).filter(song_locations.date >= displayfrom).filter(song_locations.date <= displayto).filter(song_locations.is_private == "False").all())

        # リスト用
        for f_user in follow_user:
            latestpins.extend(db.session.query(song_locations).filter(song_locations.user_id == f_user.followed_user_id).filter(song_locations.date >= displayfrom).filter(song_locations.date <= displayto).order_by(desc(song_locations.id)).limit(3).all())

        # for f_user in follow_user:
        #     latestfollow_pins = db.session.query(song_locations).filter(song_locations.user_id == f_user.followed_user_id).filter(song_locations.date >= displayfrom).filter(song_locations.date <= displayto).order_by(desc(song_locations.id)).limit(3).all()
        # for follow_pin in latestfollow_pins:
        #     latestpins.append(follow_pin)


    if status == "artist":
        # 地図用
        my_subpins = db.session.query(song_locations).filter(song_locations.user_id == login_user_id).all()
        for my_subpin in my_subpins:
                song = db.session.query(songs).filter(songs.track_id == my_subpin.track_id).filter(songs.artist_name == artist).first()
                if song:
                    pins.append(my_subpin)
        
        for user in follow_user:
            subpins = db.session.query(song_locations).filter(song_locations.user_id == user.followed_user_id).filter(song_locations.is_private == "False").all()
            for subpin in subpins:
                song = db.session.query(songs).filter(songs.track_id == subpin.track_id).filter(songs.artist_name == artist).first()
                if song:
                    pins.append(subpin)

        # 直近追加されたリスト用
        # 一回あきらめて地図と同じ内容表示させるだけにしました
        for user in follow_user:
            subpins = db.session.query(song_locations).filter(song_locations.user_id == user.followed_user_id).filter(song_locations.is_private == "False").all()
            for subpin in subpins:
                song = db.session.query(songs).filter(songs.track_id == subpin.track_id).filter(songs.artist_name == artist).first()
                if song:
                    latestpins.append(subpin)

    if status == "song_name":
        my_subpins = db.session.query(song_locations).filter(song_locations.user_id == login_user_id).all()
        for my_subpin in my_subpins:
                song = db.session.query(songs).filter(songs.track_id == my_subpin.track_id).filter(songs.track_name == song_name).first()
                if song:
                    pins.append(my_subpin)

        for user in follow_user:
            subpins = db.session.query(song_locations).filter(song_locations.user_id == user.followed_user_id).filter(song_locations.is_private == "False").all()
            for subpin in subpins:
                song = db.session.query(songs).filter(songs.track_id == subpin.track_id).filter(songs.track_name == song_name).first()
                if song:
                    pins.append(subpin)

        # 直近追加されたリスト用
        # 一回あきらめて地図と同じ内容表示させるだけにしました    
        for user in follow_user:
            subpins = db.session.query(song_locations).filter(song_locations.user_id == user.followed_user_id).filter(song_locations.is_private == "False").all()
            for subpin in subpins:
                song = db.session.query(songs).filter(songs.track_id == subpin.track_id).filter(songs.track_name == song_name).first()
                if song:
                    latestpins.append(subpin)
    
    for pin in pins:
        user_nicname = db.session.query(users.nickname).filter(users.id == pin.user_id).first()
        song = db.session.query(songs).filter(songs.track_id == pin.track_id).first()
        songdata.append({'id':pin.id,'lat':pin.latitude, 'lng':pin.longitude, 'date':pin.date.strftime("%Y-%m-%d"),'artist':song.artist_name, 'track':song.track_name, 'image':song.track_image ,'link':song.spotify_url, 'user_id':pin.user_id, 'emotion':pin.emotion, 'comment':pin.comment, 'is_private':pin.is_private, 'user_nickname': user_nicname[0]})

    for pin in latestpins:
        song = db.session.query(songs).filter(songs.track_id == pin.track_id).first()
        user = db.session.query(users).filter(users.id == pin.user_id).first()

        if db.session.query(exists().where(likes.song_location_id == pin.id).where(likes.user_id == login_user_id)).scalar() == True:
            print("True")
            latestsongdata.append({'like':'yes','id':pin.id,'lat':pin.latitude, 'lng':pin.longitude, 'date':pin.date.strftime("%Y-%m-%d"),
            'artist':song.artist_name, 'track':song.track_name, 'image':song.track_image ,'link':song.spotify_url, 'track_id':song.track_id, 'user_id':pin.user_id, 'emotion':pin.emotion, 'about':pin.about, 'comment':pin.comment, 'is_private':pin.is_private, 'user_nickname':user.nickname})
        else:
            latestsongdata.append({'like':'no','id':pin.id,'lat':pin.latitude, 'lng':pin.longitude, 'date':pin.date.strftime("%Y-%m-%d"),
            'artist':song.artist_name, 'track':song.track_name, 'image':song.track_image ,'link':song.spotify_url, 'track_id':song.track_id, 'user_id':pin.user_id, 'emotion':pin.emotion, 'about':pin.about, 'comment':pin.comment, 'is_private':pin.is_private, 'user_nickname':user.nickname})

        # latestsongdata.append({'id':pin.id,'lat':pin.latitude, 'lng':pin.longitude, 'date':pin.date.strftime("%Y-%m-%d"),
        # 'artist':song.artist_name, 'track':song.track_name, 'image':song.track_image ,'link':song.spotify_url, 'user_id':pin.user_id, 'emotion':pin.emotion, 'comment':pin.comment, 'is_private':pin.is_private, 'user_nickname':user.nickname ,'track_id':pin.track_id, 'about':pin.about })

    # profile_infomation = dict(songdata=songdata, googlemapURL=googlemapURL, user_info=user_info)
    # return profile_infomation
    home_infomation = dict(songdata=songdata, googlemapURL=googlemapURL, user_info=user_info, latestsongdata = latestsongdata)
    return home_infomation