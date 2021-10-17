
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

    // 位置情報、日付をgetTrackに送る
    $("#adding").click(function() {
      // var user_id = {{ user_id }};
      var lat = event.latLng.lat() ;
      var lng = event.latLng.lng() ;
      var date = document.getElementById("date").value;
      var emotion = document.getElementById("emotion").value;
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
        url:'/getTrack',
        data: {
          "lat":lat,
          "lng":lng,
          "date":date,
          "emotion":emotion,
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
      })
    })
  }
}
