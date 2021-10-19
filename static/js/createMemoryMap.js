
let map;
let mainMarker;
let marker =[];
let infoWindow = [];

function initMap() {
  console.log(Lat)
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


// $(document).ready(function () {
//   $("#get_song").click(function() {
//     var lat = document.getElementById("lat").value;
//     var lng = document.getElementById("lng").value;
//     var date = document.getElementById("date").value;
//     $.ajax({
//       type:'POST',
//       url:'/new_get_track',
//       data: {
//         "lat":Lat,
//         "lng":Lng,
//         "date":date
//       },
//       dataType: 'text',
//     }).done(function(){
//       console.log("success");
//       window.location.href = "/create_memory/emotion";
//     }).fail(function(){
//       console.log('failed');
//     });
//     });
// });