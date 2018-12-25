function page_goto(page){
    if(page==''){
        page = 1;
    }
    var reg = /page=\d{0,2}/;
    var url = window.location.href;

    //判断是否有参数
    if(reg.test(window.location.href)){
        url = url.replace(reg, 'page=' + page);
    }else if(url.indexOf("?") == -1){
        url = url + '?page=' + page;
    }else{
        url = url + '&page=' + page;
    }
    //重定向
    window.location.href = url;
}

// 滚动动画
$(function () {
    $(window).scroll(function(){
        //开始监听滚动条
        //获取当前滚动条高度
        var top = $(document).scrollTop();
        // var hot_top = $("#hot").offset().top;
        var random_top = $("#random").offset().top;
        var latest_top = $("#latest").offset().top;
        // 页面高度
        var height = $(window).height() - 50;
        //用于调试 弹出当前滚动条高度
        //alert(hot_height);

        //判断如果滚动条大于90则弹出 "ok"

        // if(top > hot_top - height ){
        //
        //     //alert("ok");
        //     $('#hot').addClass("fadeIn");
        // }

        if(top > random_top - height ){
            $('#random').addClass("fadeIn");
        }
        if(top > latest_top - height ){

            // alert("ok");
            $('#latest').addClass("fadeIn");
        }

    })
});

setInterval(function () {

    var d, s = "";
    var x = new Array("星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六");
    d = new Date();
    s += d.getFullYear() + "年" + (d.getMonth() + 1) + "月" + d.getDate() + "日 ";
    s += d.getHours() + "时" + (d.getMinutes()) + "分" + d.getSeconds() + "秒 ";
    s += x[d.getDay()];
    $("#time").text(s);
}, 1000);

// ajax加载博客

// 翻页
function page_jump(){
    var page = $("#page_goto input[type=text]")[0].value;
    page_goto(page);
}

// 点赞更新
function likeChange(obj, content_type, object_id){
    var is_like = obj.getElementsByClassName('active').length == 0
    $.ajax({
        url: "{% url 'likes:like_change' %}",
        type: 'GET',
        data: {
            content_type: content_type,
            object_id: object_id,
            is_like: is_like
        },
        cache: false,
        success: function(data){
            console.log(data)
            if(data['status']=='SUCCESS'){
                // 更新点赞状态
                var element = $(obj.getElementsByClassName('glyphicon'));
                if(is_like){
                    element.addClass('active');
                }else{
                    element.removeClass('active');
                }
                 // 更新点赞数量
                var liked_num = $(obj.getElementsByClassName('liked-num'));
                liked_num.text(data['liked_num']);
            }else{
                if(data['code']==400){
                     $('#login_modal').modal('show');
                }
                else{
                    alert(data['message']);
                }
            }
        },
        error: function(xhr){
            console.log(xhr)
        }
    });
}
