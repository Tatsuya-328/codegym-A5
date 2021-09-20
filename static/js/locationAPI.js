$(function () {
    $('get_location').click(function () {
        // ユーザーの端末がGeoLocation APIに対応しているかの判定
      
        // // 対応している場合
        // if( navigator.geolocation )
        // {
        //   // 現在地を取得
        //   navigator.geolocation.getCurrentPosition(
      
        //     // [第1引数] 取得に成功した場合の関数
        //     function( position )
        //     {s
        //       // 取得したデータの整理
        //       var data = position.coords ;
      
        //       // データの整理
        //       var lat = data.latitude ;
        //       var lng = data.longitude ;
      
        //     },
      
        //     // [第2引数] 取得に失敗した場合の関数
        //     function( error )
        //     {
           
      
        //       // エラー番号に対応したメッセージ
        //       var errorInfo = [
        //         "原因不明のエラーが発生しました…。" ,
        //         "位置情報の取得が許可されませんでした…。" ,
        //         "電波状況などで位置情報が取得できませんでした…。" ,
        //         "位置情報の取得に時間がかかり過ぎてタイムアウトしました…。"
        //       ] ;
      
        //       // エラー番号
        //       var errorNo = error.code ;
      
        //       // エラーメッセージ
        //       var errorMessage = "[エラー番号: " + errorNo + "]\n" + errorInfo[ errorNo ] ;
      
        //       // アラート表示
        //       alert( errorMessage ) ;
      
        //       // HTMLに書き出し
        //       document.getElementById("result").innerHTML = errorMessage;
        //     } ,
      
        //     // [第3引数] オプション
        //     {
        //       "enableHighAccuracy": false,
        //       "timeout": 8000,
        //       "maximumAge": 2000,
        //     }
      
        //   ) ;
        
        //   }

        // Ajax通信を開始する
        $.ajax({
          url: '/getTrack',
          type: 'post',
          data: 'dataだよおお'
      }).done(function(data){
          console.log(data);
      }).fail(function(){
          console.log('failed');
      });
    });
});

$(window).load(init());

function init() {
  $("#button").click(function() {
    var textData = JSON.stringify({"text":$("#input-text").val()});
    $.ajax({
      type:'POST',
      url:'/postText',
      data:textData,
      contentType:'application/json',
      success:function(data) {
        var result = JSON.parse(data.ResultSet).result;
        $("#hello").text(result);
      }
    });
    return false;
  });
}