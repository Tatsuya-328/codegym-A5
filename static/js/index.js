//  表示期間切り替え
function period(){
  var url = "/home/period/";
  let from = document.getElementById('from').value;
  let newfrom = from.replace(/\//g,"-");

  let to = document.getElementById('to').value;
  let newtill = to.replace(/\//g,"-");
  if (from == "" || to == ""){
    location.href = "/";
  }else{
    if( document.getElementById('from').value ){
      url += newfrom;
    }
    if( document.getElementById('to').value ){
        url += '/' + newtill;
    }
    location.href = url;
  }
}
function emotion(){
  var url = "/home/emotion/";
  let emotion = document.getElementById('emotion').value;
  if (emotion == "none"){
    location.href = "/";
  }else{
    url += emotion;
    location.href = url;
  }
}
function about(){
  var url = "/home/about/";
  let about = document.getElementById('about').value;
  if (about == "none"){
    location.href = "/";
  }else{
    url += about;
    location.href = url;
  }
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

function initMap() {
  var map = new google.maps.Map(document.getElementById('map'), {
      zoom: 5,
      center: {lat: 37.665498, lng: 137.75964},
      styles: 
      // mapサイト引用ここから
      [
        {
            "featureType": "all",
            "elementType": "all",
            "stylers": [
                {
                    "visibility": "on"
                }
            ]
        },
        {
            "featureType": "administrative",
            "elementType": "labels.text.fill",
            "stylers": [
                {
                    "color": "#444444"
                }
            ]
        },
        {
            "featureType": "administrative.province",
            "elementType": "all",
            "stylers": [
                {
                    "visibility": "off"
                }
            ]
        },
        {
            "featureType": "administrative.locality",
            "elementType": "all",
            "stylers": [
                {
                    "visibility": "off"
                }
            ]
        },
        {
            "featureType": "administrative.neighborhood",
            "elementType": "all",
            "stylers": [
                {
                    "visibility": "off"
                }
            ]
        },
        {
            "featureType": "administrative.land_parcel",
            "elementType": "all",
            "stylers": [
                {
                    "visibility": "off"
                }
            ]
        },
        {
            "featureType": "administrative.land_parcel",
            "elementType": "labels.text",
            "stylers": [
                {
                    "visibility": "off"
                }
            ]
        },
        {
            "featureType": "landscape",
            "elementType": "all",
            "stylers": [
                {
                    "color": "#f2f2f2"
                }
            ]
        },
        {
            "featureType": "landscape.man_made",
            "elementType": "all",
            "stylers": [
                {
                    "visibility": "simplified"
                }
            ]
        },
        {
            "featureType": "poi",
            "elementType": "all",
            "stylers": [
                {
                    "visibility": "off"
                },
                {
                    "color": "#cee9de"
                },
                {
                    "saturation": "2"
                },
                {
                    "weight": "0.80"
                }
            ]
        },
        {
            "featureType": "poi.attraction",
            "elementType": "geometry.fill",
            "stylers": [
                {
                    "visibility": "off"
                }
            ]
        },
        {
            "featureType": "poi.park",
            "elementType": "all",
            "stylers": [
                {
                    "visibility": "on"
                }
            ]
        },
        {
            "featureType": "road",
            "elementType": "all",
            "stylers": [
                {
                    "saturation": -100
                },
                {
                    "lightness": 45
                }
            ]
        },
        {
            "featureType": "road.highway",
            "elementType": "all",
            "stylers": [
                {
                    "visibility": "simplified"
                }
            ]
        },
        {
            "featureType": "road.highway",
            "elementType": "geometry.fill",
            "stylers": [
                {
                    "visibility": "on"
                },
                {
                    "color": "#f5d6d6"
                }
            ]
        },
        {
            "featureType": "road.highway",
            "elementType": "labels.text",
            "stylers": [
                {
                    "visibility": "off"
                }
            ]
        },
        {
            "featureType": "road.highway",
            "elementType": "labels.icon",
            "stylers": [
                {
                    "hue": "#ff0000"
                },
                {
                    "visibility": "on"
                }
            ]
        },
        {
            "featureType": "road.highway.controlled_access",
            "elementType": "labels.text",
            "stylers": [
                {
                    "visibility": "simplified"
                }
            ]
        },
        {
            "featureType": "road.highway.controlled_access",
            "elementType": "labels.icon",
            "stylers": [
                {
                    "visibility": "on"
                },
                {
                    "hue": "#0064ff"
                },
                {
                    "gamma": "1.44"
                },
                {
                    "lightness": "-3"
                },
                {
                    "weight": "1.69"
                }
            ]
        },
        {
            "featureType": "road.arterial",
            "elementType": "all",
            "stylers": [
                {
                    "visibility": "on"
                }
            ]
        },
        {
            "featureType": "road.arterial",
            "elementType": "labels.text",
            "stylers": [
                {
                    "visibility": "off"
                }
            ]
        },
        {
            "featureType": "road.arterial",
            "elementType": "labels.icon",
            "stylers": [
                {
                    "visibility": "off"
                }
            ]
        },
        {
            "featureType": "road.local",
            "elementType": "all",
            "stylers": [
                {
                    "visibility": "on"
                }
            ]
        },
        {
            "featureType": "road.local",
            "elementType": "labels.text",
            "stylers": [
                {
                    "visibility": "simplified"
                },
                {
                    "weight": "0.31"
                },
                {
                    "gamma": "1.43"
                },
                {
                    "lightness": "-5"
                },
                {
                    "saturation": "-22"
                }
            ]
        },
        {
            "featureType": "transit",
            "elementType": "all",
            "stylers": [
                {
                    "visibility": "off"
                }
            ]
        },
        {
            "featureType": "transit.line",
            "elementType": "all",
            "stylers": [
                {
                    "visibility": "on"
                },
                {
                    "hue": "#ff0000"
                }
            ]
        },
        {
            "featureType": "transit.station.airport",
            "elementType": "all",
            "stylers": [
                {
                    "visibility": "simplified"
                },
                {
                    "hue": "#ff0045"
                }
            ]
        },
        {
            "featureType": "transit.station.bus",
            "elementType": "all",
            "stylers": [
                {
                    "visibility": "on"
                },
                {
                    "hue": "#00d1ff"
                }
            ]
        },
        {
            "featureType": "transit.station.bus",
            "elementType": "labels.text",
            "stylers": [
                {
                    "visibility": "simplified"
                }
            ]
        },
        {
            "featureType": "transit.station.rail",
            "elementType": "all",
            "stylers": [
                {
                    "visibility": "simplified"
                },
                {
                    "hue": "#00cbff"
                }
            ]
        },
        {
            "featureType": "transit.station.rail",
            "elementType": "labels.text",
            "stylers": [
                {
                    "visibility": "simplified"
                }
            ]
        },
        {
            "featureType": "water",
            "elementType": "all",
            "stylers": [
                {
                    "color": "#46bcec"
                },
                {
                    "visibility": "on"
                }
            ]
        },
        {
            "featureType": "water",
            "elementType": "geometry.fill",
            "stylers": [
                {
                    "weight": "1.61"
                },
                {
                    "color": "#cde2e5"
                },
                {
                    "visibility": "on"
                }
            ]
        }
    ]
        // mapのサイト引用ここまで
        
        ,
        mapTypeControl: false,
        panControl: false,
        zoomControl: false,
        scaleControl: false,
        streetViewControl: false,
        fullscreenControl:false,
    });
// // 絞り込みボタン設定
//     var ingressButtonDiv = document.createElement("div");
//     var ingressButton = new ingressControl(ingressButtonDiv, map);
    
//     ingressButtonDiv.index = 1;
//     map.controls[google.maps.ControlPosition.TOP_RIGHT].push(ingressButtonDiv);
 
  console.log(SongData);

//   // 絞り込みボタン設置
//   function ingressControl(buttonDiv, map) {
//     var buttonUI = document.createElement("div");
//     buttonUI.innerHTML = "<i class='fas fa-history  fa-4x'></i>"; //ここでアイコン指定
//     buttonDiv.style.padding = "15px";
//     buttonDiv.style.color = "rgb(183, 182, 182)";
//     buttonDiv.appendChild(buttonUI);
  
//     google.maps.event.addDomListener(buttonUI, "click", function() {
//       // optionで開く設定。
//       var options ={"show":true}
//       $('#modalForm').modal(options);
//     });
//   }


  // 複数ピンを立てる
  for (var i = 0; i < SongData.length; i++) {
  
    // マーカーの追加
    marker[i] = new google.maps.Marker({
      position: new google.maps.LatLng( SongData[i]['lat'], SongData[i]['lng']),
      map: map,
      icon: SongData[i]['image'],
    });

    // 吹き出し作成
    var box_node = document.createElement('div');
    var p_node_date = document.createElement('p');
    var text_node_date = document.createTextNode(SongData[i]["date"]);
    p_node_date.appendChild(text_node_date);
    box_node.appendChild(p_node_date);

    var div_node_nickname = document.createElement('div');
    var text_node_nickname = document.createTextNode("Nickname：" + SongData[i]["user_nickname"]);
    div_node_nickname.appendChild(text_node_nickname);
    box_node.appendChild(div_node_nickname);

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
    a_node_spotify.target = "_blank"; //別タブの方がいいかなと思って追記（たつや）
    var text_node_spotify = document.createTextNode("Open Spotify");
    a_node_spotify.appendChild(text_node_spotify);
    p_node_spotify.appendChild(a_node_spotify);
    box_node.appendChild(p_node_spotify);

    // userのProfile別タブで開く
    var p_node_userlink = document.createElement("p");
    var a_node_userlink = document.createElement("a");
    a_node_userlink.href = "profile/" + SongData[i]["user_id"];
    a_node_userlink.target = "_blank";
    var text_node_userlink = document.createTextNode("Open User's page");
    a_node_userlink.appendChild(text_node_userlink);
    p_node_userlink.appendChild(a_node_userlink);
    box_node.appendChild(p_node_userlink);

    // 自分の作ったピンしか編集ボタンを表示しない
    console.log(UserId)
    if (UserId == SongData[i]["user_id"]){
      var div_edit_delete = document.createElement("div");

      var p_node_edit = document.createElement("p");
      var a_node_edit = document.createElement("a");
      a_node_edit.href = "/map/" + SongData[i]["id"] + "/edit";
      var text_node_edit = document.createTextNode("編集");
      a_node_edit.appendChild(text_node_edit);
      p_node_edit.appendChild(a_node_edit);
      p_node_edit.style.display = "inline-block";
      p_node_edit.style.margin= "0 5px";
      div_edit_delete.appendChild(p_node_edit);

      var p_node_delete = document.createElement("p");
      var a_node_delete = document.createElement("a");
      a_node_delete.href = "/map/" + SongData[i]["id"] + "/delete";
      var text_node_delete = document.createTextNode("削除");
      a_node_delete.appendChild(text_node_delete);
      p_node_delete.appendChild(a_node_delete);
      p_node_delete.style.display = "inline-block";
      p_node_delete.style.margin= "0 5px";
      div_edit_delete.appendChild(p_node_delete);

      box_node.appendChild(div_edit_delete);
    }

    // 吹き出しの追加
    infoWindow[i] = new google.maps.InfoWindow({
    // 吹き出しに詳細を追加（ほんとはboxをはりつけたい。）
    content: box_node
    });

    markerEvent(i); 
  }

  // マーカークリック時に吹き出しを表示する（複数ピンに対して）
  function markerEvent(i) {
    marker[i].addListener('click', function() {
      infoWindow[i].open(map, marker[i]); //一つの時とmakerの変数が違うから注意
    });
  }
//  複数ピンをたてるここまで。
}