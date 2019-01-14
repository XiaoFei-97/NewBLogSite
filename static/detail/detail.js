//开启高亮
$(window).load(function () {
    $("pre").addClass("prettyprint linenums");
    prettyPrint();

    id_text.placeholder("让评论多一点真诚，少一点套路~");
});

String.prototype.format = function(){
    //因为javascript中没有占位或其他可以方法可以补充,所以需要自己创建一个函数将其实现类似于占位的方式
    var str = this;
    for (var i=0;i<arguments.length; i++){
        //正则全替换
        var str = str.replace(new RegExp('\\{'+ i +'\\}', 'g'), arguments[i])
    };
    return str;
};

var clickHandler = function(){
    $('#share_addr').html(window.location.href);

};

// 关闭右键模式
// $('#post-body').contextmenu(function(event) {
//     event.preventDefault();
// });

function reply(reply_comment_id){
    // 设置值
    $('#reply_comment_id').val(reply_comment_id);
    var text = $("#comment_" + reply_comment_id).text();
    $('#reply_content').text(text);
    $('#reply_content_container').show();
    $('html').animate({scrollTop: $('#comment_form').offset().top - 120}, 300, function(){
        id_text.focus();
    });
}

function numFormat(num){
    return ('00' + num).substr(-2);
}

function timeFormat(timestamp){
    //因为js是的时间戳是以毫秒为单位的,而python是以秒为单位,所以要乘以1000
    var datetime = new Date(timestamp * 1000);
    var year = datetime.getFullYear();
    var month = numFormat(datetime.getMonth() + 1);
    var day = numFormat(datetime.getDate());
    var hour = numFormat(datetime.getHours());
    var minute = numFormat(datetime.getMinutes());
    var second = numFormat(datetime.getSeconds());
    return year + '-' + month + '-' + day + ' ' + hour + ':' + minute + ':' + second;
}

UE.Editor.prototype.placeholder = function (justPlainText) {
    var _editor = this;
    _editor.addListener("focus", function () {
        var localHtml = _editor.getPlainTxt();
        if ($.trim(localHtml) === $.trim(justPlainText)) {
            _editor.setContent(" ");
        }
    });
    _editor.addListener("blur", function () {
        var localHtml = _editor.getContent();
        if (!localHtml) {
            //_editor.setContent("<span>" + justPlainText + "</span>");
            _editor.setContent("<span style="+"color:#999;"+ ">" + justPlainText + "</span>");
        }
    });
    _editor.ready(function () {
        _editor.fireEvent("blur");
    });
};

// ueditor编辑框提交
$("#comment_form").submit(function(){
    // 判断是否为空

    if(id_text.getContent() == '' ){
        $("#comment_error").text('您尚未写任何评论内容');

        return false;
    }
    if(id_text.getContent().includes("让评论多一点真诚，少一点套路~") ){
        $("#comment_error").text('您尚未写任何评论内容');

        return false;
    }

    // 更新数据到textarea
    // id_text.updateElement();
    // 异步提交
    $.ajax({
        url: "{% url 'comment:update_comment' %}",
        type: 'POST',
        data: $(this).serialize(),
        cache: false,
        success: function(data){
            console.log(data);
            if(data['status']=="SUCCESS"){
                if($('#reply_comment_id').val()=='0'){
                    // 插入评论
                    var comment_html = '<div id="root_{0}" class="comment">' +
                        '<span>{1}</span>' +
                        '<span>({2})：</span>' +
                        '<div id="comment_{0}">{3}</div>' +
                        '<div class="like" onclick="likeChange(this, \'{4}\', {0})">' +
                            '<span class="glyphicon glyphicon-thumbs-up"></span> ' +
                            '<span class="liked-num">0</span>' +
                        '</div>' +
                        '<a href="javascript:reply({0});">回复</a>' +
                        '</div>';
                    comment_html = comment_html.format(data['pk'], data['username'], timeFormat(data['comment_time']), data['text'], data['content_type']);
                    $("#comment_list").prepend(comment_html);
                }else{
                    // 插入回复
                    var reply_html = '<div class="reply">' +
                                '<span>{1}</span>' +
                                '<span>({2})</span>' +
                                '<span>回复</span>' +
                                '<span>{3}：</span>' +
                                '<div id="comment_{0}">{4}</div>' +
                                '<div class="like" onclick="likeChange(this, \'{5}\', {0})">' +
                                    '<span class="glyphicon glyphicon-thumbs-up\"></span> ' +
                                    '<span class="liked-num">0</span>' +
                                '</div>' +
                                '<a href="javascript:reply({0});">回复</a>' +
                            '</div>';
                    reply_html = reply_html.format(data['pk'], data['username'], timeFormat(data['comment_time']), data['reply_to'], data['text'], data['content_type']);
                    $("#root_" + data['root_pk']).append(reply_html);
                }

                // 清空编辑框的内容
                id_text.setContent('');
                $('#reply_content_container').hide();
                $('#reply_comment_id').val('0');
                $('#no_comment').remove();
                window.location.reload();
                $("#comment_error").text('评论成功');
            }else{
                // 显示错误信息
                $("#comment_error").text(data['message']);
            }
        },
        error: function(xhr){
            console.log(xhr);
        }
    });
    return false;
});

/**文章目录*/
$(function () {
    var oDiv = document.getElementById("blogMenu"),
        H = 0,
        Y = oDiv;
    while (Y) {
        H += Y.offsetTop;
        Y = Y.offsetParent;
    }
    window.onscroll = function()
    {
        var s = document.body.scrollTop || document.documentElement.scrollTop;
        if(s>H-50) {
            oDiv.style = "position:fixed;top:30px;";
        } else {
            oDiv.style = ""
        }
    };

});

/**
* ckeditor编辑框的提交
$("#comment_form").submit(function(){
// 判断是否为空

if(CKEDITOR.instances["id_text"].document.getBody().getText().trim()==''){
    $("#comment_error").text('您尚未写任何评论内容');

    return false;
}

// 更新数据到textarea
CKEDITOR.instances['id_text'].updateElement();
// 异步提交
$.ajax({
    url: "{% url 'comment:update_comment' %}",
    type: 'POST',
    data: $(this).serialize(),
    cache: false,
    success: function(data){
        console.log(data);
        if(data['status']=="SUCCESS"){
            if($('#reply_comment_id').val()=='0'){
                // 插入评论
                var comment_html = '<div id="root_{0}" class="comment">' +
                    '<span>{1}</span>' +
                    '<span>({2})：</span>' +
                    '<div id="comment_{0}">{3}</div>' +
                    '<div class="like" onclick="likeChange(this, \'{4}\', {0})">' +
                        '<span class="glyphicon glyphicon-thumbs-up"></span> ' +
                        '<span class="liked-num">0</span>' +
                    '</div>' +
                    '<a href="javascript:reply({0});">回复</a>' +
                    '</div>';
                comment_html = comment_html.format(data['pk'], data['username'], timeFormat(data['comment_time']), data['text'], data['content_type']);
                $("#comment_list").prepend(comment_html);
            }else{
                // 插入回复
                var reply_html = '<div class="reply">' +
                            '<span>{1}</span>' +
                            '<span>({2})</span>' +
                            '<span>回复</span>' +
                            '<span>{3}：</span>' +
                            '<div id="comment_{0}">{4}</div>' +
                            '<div class="like" onclick="likeChange(this, \'{5}\', {0})">' +
                                '<span class="glyphicon glyphicon-thumbs-up\"></span> ' +
                                '<span class="liked-num">0</span>' +
                            '</div>' +
                            '<a href="javascript:reply({0});">回复</a>' +
                        '</div>';
                reply_html = reply_html.format(data['pk'], data['username'], timeFormat(data['comment_time']), data['reply_to'], data['text'], data['content_type']);
                $("#root_" + data['root_pk']).append(reply_html);
            }

            // 清空编辑框的内容
            CKEDITOR.instances['id_text'].setData('');
            $('#reply_content_container').hide();
            $('#reply_comment_id').val('0');
            $('#no_comment').remove();
            window.location.reload();
            $("#comment_error").text('评论成功');
        }else{
            // 显示错误信息
            $("#comment_error").text(data['message']);
        }
    },
    error: function(xhr){
        console.log(xhr);
    }
});
return false;
});
**/

//更新点赞状态
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