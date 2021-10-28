//  表示期間切り替え 
function period(){
  var url = "/profile/" + UserInfo.id + "/period/";
  let from = document.getElementById('from').value;
  let newfrom = from.replace(/\//g,"-");

  let to = document.getElementById('to').value;
  let newtill = to.replace(/\//g,"-");
  if (from == "" || to == ""){
    var rooturl ="/profile/" + UserInfo.id;
    location.href = rooturl;
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
  var url = "/profile/" + UserInfo.id;
  let emotion = document.getElementById('emotion').value;
  if (emotion == "none"){
    location.href = url;
  }else{
    url += "/emotion/";
    url += emotion;
    location.href = url;
  }
}

function about(){
  var url = "/profile/" + UserInfo.id;
  let about = document.getElementById('about').value;
  if (about == "none"){
    location.href = url;
  }else{
    url += "/about/";
    url += about;
    location.href = url;
  }
}
function artist(){
  var url = "/profile/" + UserInfo.id + "/artist/";
  let artist = document.getElementById('artist').value;
  url += artist;
  location.href = url;
}

function song_name(){
  var url = "/profile/" + UserInfo.id + "/song_name/";
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
  // 地図表示
  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 4,
    center: {lat: 37.065498, lng: 139.75964},
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
  // 絞り込みボタン設定
  var ingressButtonDiv = document.createElement("div");
  var ingressButton = new ingressControl(ingressButtonDiv, map);
    
  ingressButtonDiv.index = 1;
  map.controls[google.maps.ControlPosition.TOP_RIGHT].push(ingressButtonDiv);

  console.log(SongData);

  // 絞り込みボタン設置
  function ingressControl(buttonDiv, map) {
    var buttonUI = document.createElement("div");
    buttonUI.innerHTML = "<i class='fas fa-history  fa-4x'></i>"; //ここでアイコン指定
    buttonDiv.style.padding = "15px";
    buttonDiv.style.color = "rgb(42, 42, 42)";
    buttonDiv.appendChild(buttonUI);

    google.maps.event.addDomListener(buttonUI, "click", function() {
      // optionで開く設定。
      var options ={"show":true}
      $('#modalForm').modal(options);
    });
  }

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