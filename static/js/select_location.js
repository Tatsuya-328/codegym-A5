// 地図関連
let map;
let mainMarker;
let marker =[];
let infoWindow = [];

function initMap() {
  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 14,
    center: {lat: 35.665498, lng: 139.75964},
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

    var p_node_artist = document.createElement('p');
    var text_node_artist = document.createTextNode("Artist：" + SongData[i]["artist"]);
    p_node_artist.appendChild(text_node_artist);
    box_node.appendChild(p_node_artist);

    var p_node_track = document.createElement('p');
    var text_node_track = document.createTextNode("曲名：" + SongData[i]["track"]);
    p_node_track.appendChild(text_node_track);
    box_node.appendChild(p_node_track);

    var p_node_emotion = document.createElement('p');
    var text_node_emotion = document.createTextNode("感情：" + SongData[i]["emotion"]);
    p_node_emotion.appendChild(text_node_emotion);
    box_node.appendChild(p_node_emotion);

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

    // 自分の作ったピンしか編集、削除ボタンを表示しない
    if (UserId == SongData[i]["user_id"]){
      console.log(SongData[i]["id"] )
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
      $.ajax({
        type:'POST',
        url:'/getTrack',
        data: {
          "lat":lat,
          "lng":lng,
          "date":date,
          "emotion":emotion,
          "comment":comment,
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