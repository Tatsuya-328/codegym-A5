
let map;
let mainMarker;
let marker =[];
let infoWindow = [];

function initMap() {
  console.log(Lat)
  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 9.5,
    center: {lat: Lat, lng: Lng},
    //   既存のマーカーがあるとごちゃごちゃするから消す
    styles: [
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

  var marker = new google.maps.Marker();
    //markerの位置を設定
    //event.latLng.lat()でクリックしたところの緯度を取得
    marker.setPosition(new google.maps.LatLng(Lat, Lng));
    //marker設置
    marker.setMap(map);
    // window表示して、今の楽曲取得して登録ボタンをつける。
    var registerbox = document.createElement('div');
    registerbox.class = "box";
    var p_node_spotify = document.createElement('p');
    var text_p_node_spotify = document.createTextNode("Spotifyで曲を再生してボタンを押してください");
    p_node_spotify.append(text_p_node_spotify);
    registerbox.appendChild(p_node_spotify);
    var a_node_spotify = document.createElement('a');
    var text_node_spotify = document.createTextNode("お気に入りリストを開く");
    a_node_spotify.href = 'https://open.spotify.com/collection/tracks';
    a_node_spotify.target = '_blank';
    a_node_spotify.appendChild(text_node_spotify);
    registerbox.appendChild(a_node_spotify);

    var infowindow = new google.maps.InfoWindow({
      content: registerbox
    });
    infowindow.open(map, marker)

    google.maps.event.addListener(marker, 'dblclick', deletelistener);
    function deletelistener(event){ 
      marker.setMap(null);
    }

  //  複数ピンをたてるここまで。

  // 後からピンを追加できるようにする
  //mapをクリックしたときのイベントを設定
  google.maps.event.addListener(map, 'click', mylistener);
  //クリックしたときの処理
  function mylistener(event){
    //marker作成
    var marker = new google.maps.Marker();
    //markerの位置を設定
    //event.latLng.lat()でクリックしたところの緯度を取得
    marker.setPosition(new google.maps.LatLng(event.latLng.lat(), event.latLng.lng()));
    document.getElementById('lat').value = event.latLng.lat();
    document.getElementById('lng').value = event.latLng.lng();
    //marker設置
    marker.setMap(map);
    // window表示して、今の楽曲取得して登録ボタンをつける。
    var registerbox = document.createElement('div');
    registerbox.class = "box";
    var p_node_spotify = document.createElement('p');
    var text_p_node_spotify = document.createTextNode("Spotifyで曲を再生してボタンを押してください");
    p_node_spotify.append(text_p_node_spotify);
    registerbox.appendChild(p_node_spotify);
    var a_node_spotify = document.createElement('a');
    var text_node_spotify = document.createTextNode("お気に入りリストを開く");
    a_node_spotify.href = 'https://open.spotify.com/collection/tracks';
    a_node_spotify.target = '_blank';
    a_node_spotify.appendChild(text_node_spotify);
    registerbox.appendChild(a_node_spotify);

    var infowindow = new google.maps.InfoWindow({
      content: registerbox
    });
    infowindow.open(map, marker)

    // マーカーをダブルクリックで削除
    google.maps.event.addListener(marker, 'dblclick', deletelistener);
    function deletelistener(event){ 
      marker.setMap(null);
    }
  }
}