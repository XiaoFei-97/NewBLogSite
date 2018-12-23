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
