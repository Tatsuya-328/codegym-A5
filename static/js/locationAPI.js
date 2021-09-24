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
            $.ajax({
              type:'POST',
              url:'/getTrack',
              data: {
                "lat":lat,
                "lng":lng
              },
              dataType: 'text',
            }).done(function(){
              console.log("success");
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

let map;
let mainMarker;
let marker =[];
let infoWindow = [];

function initMap() {
  let SongData = [{'lat':'35.681236', 'lng':'139.767125',  'date':'2020/3/9', 'artist':'KOBUKURO', 'track':'桜', 'image':'https://i.scdn.co/image/ab67616d00004851584f8b783934669d26a7891f' ,'link':'https://open.spotify.com/track/5Hi4IAtdFZzg6IfAVMd6lZ'},
                    {'lat':'35.665498', 'lng':'139.75964',  'date':'2019/9/1', 'artist':'Daoko, Kenshi Yonezu', 'track':'打上花火', 'image':'https://i.scdn.co/image/ab67616d00004851e7f0b1cfcf4da8333f7644aa','link':'https://open.spotify.com/track/4IouQaO9GkaHC7AtMErdSa'},
                    {'lat':'35.675069', 'lng':'139.763328',  'date':'2021/12/24', 'artist':'back number', 'track':'クリスマスソング', 'image':'https://i.scdn.co/image/ab67616d0000485159a14a1d53eb5610f84c8382','link':'https://open.spotify.com/track/5P8ZvBQoCrujjNcLAxO3Su'},
                    ];

  var map = new google.maps.Map(document.getElementById('map'), {
      zoom: 14,
      center: {lat: 35.665498, lng: 139.75964}
  });

  // 一つだけピンを立てる
  var marker = new google.maps.Marker({
    position: {lat: 35.678655, lng:139.748318},
    map: map,
    icon: "https://i.scdn.co/image/ab67616d00004851ba5db46f4b838ef6027e6f96"
  });

  var onebox = '<div class="box">' + 
            '<p>2020年9月1日</p>' +
            '<p>Artist: Ed Sheeran</p>' +
            '<p>Truck: Shape of You </p>' +
              '<a href = "https://api.spotify.com/v1/tracks/7qiZfU4dY1lWllzX7mPBI3">Open Spotify</a>' +
            '</div>'

  var infowindow = new google.maps.InfoWindow({
    content: onebox
  });

   // クリックしたら詳細がでる。
   oneEvent();

   function oneEvent() {
     marker.addListener('click', function() {
       infowindow.open(map, marker);
     });
   }

  // 複数ピンを立てる
  for (var i = 0; i < SongData.length; i++) {
  
    // マーカーの追加
    marker[i] = new google.maps.Marker({
      // position: '{lat:'+ SongData[i]["lat"] + 'lng: ' + SongData[i]["lng"] + '}',
      position: new google.maps.LatLng( SongData[i]['lat'], SongData[i]['lng']),
      map: map,
      icon: SongData[i]['image'],
    });

    // 吹き出しの内容
    box = '<div class="box">' + 
    '<p>SongData[i]["date"]</p>' +
    '<p>Artist: SongData[i]["artist"]</p>' +
    '<p>Truck:SongData[i]["track"]</p>' +
      '<a href = SongData[i]["link"]>Open Spotify</a>' +
    '</div>'

    // 吹き出しの追加
    infoWindow[i] = new google.maps.InfoWindow({
    // 吹き出しに詳細を追加
    content: 'Date' + SongData[i]["date"] + 'Artist' + SongData[i]["artist"] + 'Track' + SongData[i]["track"] +  'Spotify' + SongData[i]["link"]
    });

    markerEvent(i); 
  }

  // マーカークリック時に吹き出しを表示する
  function markerEvent(i) {
    marker[i].addListener('click', function() {
      infoWindow[i].open(map, marker[i]);
    });
  }
 
}


