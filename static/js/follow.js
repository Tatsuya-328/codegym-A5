$(document).ready(function () {
  // フォロー
  $("#follow").click(function() {
    user_id = "111";
    $.ajax({
        type:'POST',
        url:'/follow',
        data: {
          "follow_or_cancell" :"follow",
          "user_id" : user_id
        },
        dataType: 'text',
      }).done(function(){
        console.log("success");
        window.location.href = '/profile';
      }).fail(function(){
        console.log('failed');
      });
  });
  $("#cancell").click(function() {
    user_id = "111";
    $.ajax({
      type:'POST',
      url:'/follow',
      data: {
        "follow_or_cancell" :"cancell",
        "user_id" : user_id
      },
      dataType: 'text',
    }).done(function(){
      console.log("success");
      window.location.href = '/profile';
    }).fail(function(){
      console.log('failed');
    });
  });
});