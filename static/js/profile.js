$(document).ready(function () {
  $("#location").click(function() {
    if( navigator.geolocation )
      {
        // 現在地を取得
        navigator.geolocation.getCurrentPosition(
          // [第1引数] 取得に成功した場合の関数
          function( position )
          {
            // 取得したデータの整理
            var data = position.coords ;
            // データの整理
            var lat = data.latitude ;
            var lng = data.longitude ;
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
            });
          },
          // [第2引数] 取得に失敗した場合の関数
          function( error )
          {
            // エラー番号に対応したメッセージ
            var errorInfo = [
              "原因不明のエラーが発生しました…。" ,
              "位置情報の取得が許可されませんでした…。" ,
              "電波状況などで位置情報が取得できませんでした…。" ,
              "位置情報の取得に時間がかかり過ぎてタイムアウトしました…。"
            ] ;
            // エラー番号
            var errorNo = error.code ;
            // エラーメッセージ
            var errorMessage = "[エラー番号: " + errorNo + "]\n" + errorInfo[ errorNo ] ;
            // アラート表示
            alert( errorMessage ) ;
            // HTMLに書き出し
            document.getElementById("result").innerHTML = errorMessage;
          } ,
          // [第3引数] オプション
          {
            "enableHighAccuracy": false,
            "timeout": 8000,
            "maximumAge": 2000,
          }
        ) ;
      }
    });
});

//  表示期間切り替え 
function period(){
  var url = "/profile/" + UserInfo.id + "/period/";
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

// 地図関連
let map;
let mainMarker;
let marker =[];
let infoWindow = [];

function initMap() {
  // 地図表示
  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 14,
    center: {lat: 35.665498, lng: 139.75964},
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

    var div_node_artist = document.createElement('div');
    var text_node_artist = document.createTextNode("Artist：" + SongData[i]["artist"]);
    div_node_artist.appendChild(text_node_artist);
    box_node.appendChild(div_node_artist);

    var p_node_track = document.createElement('div');
    var text_node_track = document.createTextNode("曲名：" + SongData[i]["track"]);
    p_node_track.appendChild(text_node_track);
    box_node.appendChild(p_node_track);

    var div_node_emotion = document.createElement('div');
    var text_node_emotion = document.createTextNode("感情：" + SongData[i]["emotion"]);
    div_node_emotion.appendChild(text_node_emotion);
    box_node.appendChild(div_node_emotion);

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
    console.log(UserId)
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

$(document).ready(function () {
    // フォロー
    $("#follow").click(function() {
        display_user_id = document.getElementById("display_user_id").textContent
        $.ajax({
            type:'POST',
            url:'/follow',
            data: {
            "follow_or_cancell" :"follow",
            "user_id" : display_user_id
            },
            dataType: 'text',
        }).done(function(){
            console.log("success");
            window.location.href = '/';
        }).fail(function(){
            console.log('failed');
        });
    });
    $("#cancell").click(function() {
        display_user_id = document.getElementById("display_user_id").textContent
        $.ajax({
        type:'POST',
        url:'/follow',
        data: {
            "follow_or_cancell" :"cancell",
            "user_id" : display_user_id
        },
        dataType: 'text',
        }).done(function(){
        console.log("success");
        window.location.href = '/';
        }).fail(function(){
        console.log('failed');
        });
    });
});

jQuery(function($){
  $('.menu').on('click',function(){
      $('.menu__line').toggleClass('active');
      $('.gnav').fadeToggle();
  });
});