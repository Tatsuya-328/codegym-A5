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
      styles:[
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
    ],
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