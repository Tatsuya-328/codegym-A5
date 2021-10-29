//  表示期間切り替え
function period(){
  var url = "/home/period/";
  let from = document.getElementById('from').value;
  let newfrom = from.replace(/\//g,"-");

  let to = document.getElementById('to').value;
  let newtill = to.replace(/\//g,"-");
  if( document.getElementById('from').value ){
    url += newfrom;
  }
  if( document.getElementById('to').value ){
    url += '/' + newtill;
  }
  location.href = url;
}
function emotion(){
  var url = "/home/emotion/";
  let emotion = document.getElementById('emotion').value;
  url += emotion;
  location.href = url;
}

function artist(){
  var url = "/home/artist/";
  let artist = document.getElementById('artist').value;
  url += artist;
  location.href = url;
}

function song_name(){
  var url = "/home/song_name/";
  let song_name = document.getElementById('song_name').value;
  url += song_name;
  location.href = url;
}

// 地図関連
let map;
let mainMarker;
let marker =[];
let infoWindow = [];


console.log(SongData)

function initMap() {
  console.log(Lat)
  console.log(Lng)
  // 地図表示
  var map = new google.maps.Map(document.getElementById('map'), {
      zoom: 14,
      center: {lat: Lat, lng: Lng},
      styles: [{
        featureType: 'poi',
        stylers: [
          { visibility: 'off' }
        ]
      },{
        featureType: 'road',
        elementType: 'labels',
        stylers: [
          { visibility: 'off' }
        ]
      },],
      mapTypeControl: false,
      panControl: false,
      zoomControl: false,
      scaleControl: false,
      streetViewControl: false,
      fullscreenControl:false,
  });
  console.log(SongData)
  // 編集するピン
  
    // マーカーの追加
    marker = new google.maps.Marker({
      position: new google.maps.LatLng( Lat, Lng),
      map: map,
      icon: SongData['image'],
    });
    console.log("su")

    // 編集フォームの作成
    var box_node = document.createElement('div');
    var p_node_date = document.createElement('p');
    var text_node_date = document.createTextNode(SongData["date"]);
    p_node_date.appendChild(text_node_date);
    box_node.appendChild(p_node_date);

    var div_node_artist = document.createElement('div');
    var text_node_artist = document.createTextNode("Artist：" + SongData["artist"]);
    div_node_artist.appendChild(text_node_artist);
    box_node.appendChild(div_node_artist);

    var div_node_track = document.createElement('div');
    var text_node_track = document.createTextNode("曲名：" + SongData["track"]);
    div_node_track.appendChild(text_node_track);
    box_node.appendChild(div_node_track);

    var div_node_emotion = document.createElement('div');
    var text_node_emotion = document.createTextNode("感情：" + SongData["emotion"]);
    div_node_emotion.appendChild(text_node_emotion);
    box_node.appendChild(div_node_emotion);

    var div_node_about = document.createElement('div');
    var text_node_about = document.createTextNode("ジャンル：" + SongData["about"]);
    div_node_about.appendChild(text_node_about);
    box_node.appendChild(div_node_about);

    var p_node_comment = document.createElement('p');
    var text_node_comment = document.createTextNode("コメント：" + SongData["comment"]);
    p_node_comment.appendChild(text_node_comment);
    box_node.appendChild(p_node_comment);

    var p_node_spotify = document.createElement("p");
    var a_node_spotify = document.createElement("a");
    a_node_spotify.href = SongData["link"];
    var text_node_spotify = document.createTextNode("Open Spotify");
    a_node_spotify.appendChild(text_node_spotify);
    p_node_spotify.appendChild(a_node_spotify);
    box_node.appendChild(p_node_spotify);

    if (UserId == SongData["user_id"]){
      console.log(SongData["id"] )
      var div_edit_delete = document.createElement("div");

      var p_node_edit = document.createElement("p");
      var a_node_edit = document.createElement("a");
      a_node_edit.href = "/map/" + SongData["id"] + "/edit";
      var text_node_edit = document.createTextNode("編集");
      a_node_edit.appendChild(text_node_edit);
      p_node_edit.appendChild(a_node_edit);
      p_node_edit.style.display = "inline-block";
      p_node_edit.style.margin= "0 5px";
      div_edit_delete.appendChild(p_node_edit);

      var p_node_delete = document.createElement("p");
      var a_node_delete = document.createElement("a");
      a_node_delete.href = "/map/" + SongData["id"] + "/delete";
      var text_node_delete = document.createTextNode("削除");
      a_node_delete.appendChild(text_node_delete);
      p_node_delete.appendChild(a_node_delete);
      p_node_delete.style.display = "inline-block";
      p_node_delete.style.margin= "0 5px";
      div_edit_delete.appendChild(p_node_delete);

      box_node.appendChild(div_edit_delete);
    }

    // 吹き出しの追加
    infoWindow = new google.maps.InfoWindow({
      content: box_node
    });

    // markerEvent(i); 
    infoWindow.open(map, marker);
  
}