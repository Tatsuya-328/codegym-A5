let map;
let mainMarker;
let marker =[];
let infoWindow = [];

function initMap() {
  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 10,
    center: {lat: Lat, lng: Lng},
    //   既存のマーカーがあるとごちゃごちゃするから消す
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
    },
    ]
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
    p_node_spotify.style = "margin: 0px;"
    var text_p_node_spotify = document.createTextNode("この場所にピンを保存します");
    p_node_spotify.append(text_p_node_spotify);
    registerbox.appendChild(p_node_spotify);

    var infowindow = new google.maps.InfoWindow({
      content: registerbox
    });
    infowindow.open(map, marker)
}
