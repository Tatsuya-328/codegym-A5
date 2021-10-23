// 地図関連
let map;
let mainMarker;
let marker =[];
let infoWindow = [];

function initMap() {
  console.log(Lat)
  console.log(Lng)
  // 地図表示
  var map = new google.maps.Map(document.getElementById('map'), {
      zoom: 14,
      center: {lat: Lat, lng: Lng},
      mapTypeControl: false,
      panControl: false,
      zoomControl: false,
      scaleControl: false,
      streetViewControl: false,
      fullscreenControl:false,
  });

  // 編集するピン
  for (var i = 0; i < SongData.length; i++) {
    // マーカーの追加
    marker[i] = new google.maps.Marker({
      position: new google.maps.LatLng( SongData[i]['lat'], SongData[i]['lng']),
      map: map,
      icon: SongData[i]['image'],
    });

    // 編集フォームの作成
    var box_node = document.createElement('div');
    var p_node_date = document.createElement('p');
    var text_node_date = document.createTextNode(SongData[i]["date"]);
    p_node_date.appendChild(text_node_date);
    box_node.appendChild(p_node_date);

    var div_node_artist = document.createElement('div');
    var text_node_artist = document.createTextNode("Artist：" + SongData[i]["artist"]);
    div_node_artist.appendChild(text_node_artist);
    box_node.appendChild(div_node_artist);

    var div_node_track = document.createElement('div');
    var text_node_track = document.createTextNode("曲名：" + SongData[i]["track"]);
    div_node_track.appendChild(text_node_track);
    box_node.appendChild(div_node_track);

    var div_node_emotion = document.createElement('div');
    var text_node_emotion = document.createTextNode("感情：" + SongData[i]["emotion"]);
    div_node_emotion.appendChild(text_node_emotion);
    box_node.appendChild(div_node_emotion);

    var div_node_about = document.createElement('div');
    var text_node_about = document.createTextNode("ジャンル：" + SongData[i]["about"]);
    div_node_about.appendChild(text_node_about);
    box_node.appendChild(div_node_about);

    var p_node_comment = document.createElement('p');
    var text_node_comment = document.createTextNode("コメント：" + SongData[i]["comment"]);
    p_node_comment.appendChild(text_node_comment);
    box_node.appendChild(p_node_comment);

    var p_node_spotify = document.createElement("p");
    var a_node_spotify = document.createElement("a");
    a_node_spotify.href = SongData[i]["link"];
    var text_node_spotify = document.createTextNode("Open Spotify");
    a_node_spotify.appendChild(text_node_spotify);
    p_node_spotify.appendChild(a_node_spotify);
    box_node.appendChild(p_node_spotify);

    // 吹き出しの追加
    infoWindow[i] = new google.maps.InfoWindow({
      content: box_node
    });

    // markerEvent(i); 
    infoWindow[i].open(map, marker[i]);
  }


  $("#update").click(function() {
    var SongDataId = SongData[0]["id"];
    console.log("success")
    var date = document.getElementById("date").value;
    var emotion = document.getElementById("emotion").value;
    var about = document.getElementById("about").value;
    var comment = document.getElementById("comment").value;
    var pin_statuses = document.getElementsByName("pin_status");
    var pin_status = ""
    for (var i = 0; i < 2; i++){
      if(pin_statuses[i].checked == true){
        pin_status = pin_statuses[i].value
        // console.log(pin_status)
      }
    }
    $.ajax({
      type:'POST',
      url:'/map/' + SongDataId + '/edit',
      data: {
        "date":date,
        "emotion":emotion,
        "about":about,
        "comment":comment,
        "pin_status":pin_status,
      },
      dataType: 'text',
    }).done(function(){
      console.log("success");
      url = "/profile/";
      url += UserId;
      window.location.href = url;
    }).fail(function(){
      console.log('failed');
    });
  })
}