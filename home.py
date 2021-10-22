from models import users, song_locations, songs, follow, made_playlists, db
from sqlalchemy import or_

def Home_info(login_user_id, status, displayfrom, displayto, emotion, artist, song_name, GOOGLE_MAP_API_KEY):
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
    googlemapURL = "https://maps.googleapis.com/maps/api/js?key="+GOOGLE_MAP_API_KEY

    
    if status == "emotion":
        pins.extend(db.session.query(song_locations).filter(song_locations.user_id == login_user_id).filter(song_locations.emotion == emotion).all())
        for user in follow_user:
            pins.extend(db.session.query(song_locations).filter(song_locations.user_id == user.followed_user_id).filter(song_locations.emotion == emotion).filter(song_locations.is_private == "False").all())

    if status == "period":
        pins.extend(db.session.query(song_locations).filter(song_locations.user_id == login_user_id).filter(song_locations.date >= displayfrom).filter(song_locations.date <= displayto).all())
        for user in follow_user:
            pins.extend(db.session.query(song_locations).filter(song_locations.user_id == user.followed_user_id).filter(song_locations.date >= displayfrom).filter(song_locations.date <= displayto).filter(song_locations.is_private == "False").all())

    if status == "artist":
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
    
    
    for pin in pins:
        user_nicname = db.session.query(users.nickname).filter(users.id == pin.user_id).first()
        song = db.session.query(songs).filter(songs.track_id == pin.track_id).first()
        songdata.append({'id':pin.id,'lat':pin.latitude, 'lng':pin.longitude, 'date':pin.date.strftime("%Y-%m-%d"),'artist':song.artist_name, 'track':song.track_name, 'image':song.track_image ,'link':song.spotify_url, 'user_id':pin.user_id, 'emotion':pin.emotion, 'comment':pin.comment, 'is_private':pin.is_private, 'user_nickname': user_nicname[0]})

    # profile_infomation = dict(songdata=songdata, googlemapURL=googlemapURL, user_info=user_info)
    # return profile_infomation
    home_infomation = dict(songdata=songdata, googlemapURL=googlemapURL, user_info=user_info)
    return home_infomation