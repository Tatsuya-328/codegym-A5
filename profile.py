from models import users, song_locations, songs, follow, made_playlists, db
from sqlalchemy import or_

def Profile_info(login_user_id, display_user_id, status, displayfrom, displayto, emotion, artist, song_name, GOOGLE_MAP_API_KEY):
    # ユーザの情報
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
    nickname = db.session.query(users.nickname).filter(users.id == display_user_id).first()
    username = db.session.query(users.username).filter(users.id == display_user_id).first()
    user_info = dict(id=display_user_id, username=username[0], following=following_status, follow_number=follow_number, followed_number=followed_number, nickname=nickname[0])
    print(user_info)
    print(nickname)

    pins = []
    songdata = []
    latestpins = []
    latestsongdata = []
    googlemapURL = "https://maps.googleapis.com/maps/api/js?key="+GOOGLE_MAP_API_KEY

    if status == "emotion":
      if login_user_id != display_user_id:
          pins = db.session.query(song_locations).filter(song_locations.user_id == display_user_id).filter(song_locations.emotion == emotion).filter(song_locations.is_private == "False").all()
        # リスト用
          latestpins = db.session.query(song_locations).filter(song_locations.user_id == display_user_id).filter(song_locations.emotion == emotion).filter(song_locations.is_private == "False").all()          
      else:
          pins = db.session.query(song_locations).filter(song_locations.user_id == display_user_id).filter(song_locations.emotion == emotion).all()
          # リスト用
          latestpins = db.session.query(song_locations).filter(song_locations.user_id == display_user_id).filter(song_locations.emotion == emotion).all()

    if status == "period":
      if login_user_id != display_user_id:
        pins = db.session.query(song_locations).filter(song_locations.user_id == display_user_id).filter(song_locations.date >= displayfrom).filter(song_locations.date <= displayto).filter(song_locations.is_private == "False").all()
        latestpins = db.session.query(song_locations).filter(song_locations.user_id == display_user_id).filter(song_locations.date >= displayfrom).filter(song_locations.date <= displayto).filter(song_locations.is_private == "False").all()
      else:
        pins = db.session.query(song_locations).filter(song_locations.user_id == display_user_id).filter(song_locations.date >= displayfrom).filter(song_locations.date <= displayto).all()
        latestpins = db.session.query(song_locations).filter(song_locations.user_id == display_user_id).filter(song_locations.date >= displayfrom).filter(song_locations.date <= displayto).all()


    if status == "artist":
      if login_user_id != display_user_id:
          pins = []
          subpins = db.session.query(song_locations).filter(song_locations.user_id == display_user_id).filter(song_locations.is_private == "False").all()
      else:
          subpins = db.session.query(song_locations).filter(song_locations.user_id == display_user_id).all()
      for subpin in subpins:
        song = db.session.query(songs).filter(songs.track_id == subpin.track_id).filter(songs.artist_name == artist).first()
        if song:
          pins.append(subpin)

# リスト用 あきらめて地図のデータそのままです
      if login_user_id != display_user_id:
          subpins = db.session.query(song_locations).filter(song_locations.user_id == display_user_id).filter(song_locations.is_private == "False").all()
      else:
          subpins = db.session.query(song_locations).filter(song_locations.user_id == display_user_id).all()
      for subpin in subpins:
        song = db.session.query(songs).filter(songs.track_id == subpin.track_id).filter(songs.artist_name == artist).first()
        if song:
          latestpins.append(subpin)

    if status == "song_name":
      if login_user_id != display_user_id:
        pins = []
        subpins = db.session.query(song_locations).filter(song_locations.user_id == display_user_id).filter(song_locations.is_private == "False").all()
      else:
          subpins = db.session.query(song_locations).filter(song_locations.user_id == display_user_id).all()
      for subpin in subpins:
        song = db.session.query(songs).filter(songs.track_id == subpin.track_id).filter(songs.track_name == song_name).first()
        if song:
          pins.append(subpin)

# リスト用 あきらめて地図のデータそのままです
      if login_user_id != display_user_id:
        subpins = db.session.query(song_locations).filter(song_locations.user_id == display_user_id).filter(song_locations.is_private == "False").all()
      else:
          subpins = db.session.query(song_locations).filter(song_locations.user_id == display_user_id).all()
      for subpin in subpins:
        song = db.session.query(songs).filter(songs.track_id == subpin.track_id).filter(songs.track_name == song_name).first()
        if song:
          latestpins.append(subpin)
      
    
    for pin in pins:
        song = db.session.query(songs).filter(songs.track_id == pin.track_id).first()
        songdata.append({'id':pin.id,'lat':pin.latitude, 'lng':pin.longitude, 'date':pin.date.strftime("%Y-%m-%d"),'artist':song.artist_name, 'track':song.track_name, 'image':song.track_image ,'link':song.spotify_url, 'user_id':pin.user_id, 'emotion':pin.emotion, 'comment':pin.comment, 'is_private':pin.is_private})

    for pin in latestpins:
        song = db.session.query(songs).filter(songs.track_id == pin.track_id).first()
        latestsongdata.append({'id':pin.id,'lat':pin.latitude, 'lng':pin.longitude, 'date':pin.date.strftime("%Y-%m-%d"),'artist':song.artist_name, 'track':song.track_name, 'image':song.track_image ,'link':song.spotify_url, 'user_id':pin.user_id, 'emotion':pin.emotion, 'comment':pin.comment, 'is_private':pin.is_private, 'track_id':pin.track_id, 'about':pin.about})
    

    profile_infomation = dict(songdata=songdata,latestsongdata=latestsongdata ,googlemapURL=googlemapURL, user_info=user_info)
    return profile_infomation