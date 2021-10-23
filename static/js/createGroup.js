$(document).ready(function () {
  // フォロー
  $("#create_group_table").click(function() {
    console.log("create_table")
    // add_users = document.getElementById("add_users").textContent
    add_users = ""
    // 追加するユーザーのリストを取得して送りたい。選択形式
    $.ajax({
        type:'POST',
        url:'/create_group_table',
        data: {
          "add_users": add_users
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