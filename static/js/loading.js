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
            $.ajax({
              type:'POST',
              url:'/getTrack',
              data: {
                "lat":lat,
                "lng":lng,
                "emotion":emotion,
                "comment":comment,
              },
              dataType: 'text',
            }).done(function(){
              console.log("success");
              window.location.href = '/';
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