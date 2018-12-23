//登录注册按钮
$(function () {
    $("#login_button").click(function () {
        $('#login_modal').modal('show');
    });
    // 注册按钮
    $("#register_button").click(function () {
        $('#register_modal').modal('show');
    });
    // 找回密码
    $("#forgot_password_button").click(function () {
        $('#login_modal').modal('hide');
        $('#forgot_password_modal').modal('show');
    });
});

// 检查搜索框
function check() {
    var key = $("#key").val();

    if(key == null || key == ""){
        // alert("搜索内容不能为空！");
        window.location.href = '/blog';
        return false;
    }
    return true;
}