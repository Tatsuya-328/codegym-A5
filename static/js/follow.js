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