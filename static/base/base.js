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

    $("#search").click(function () {
        $("header").toggleClass("search-header");
        $(".search").toggle();
    });

    setInterval(formatTime,1000);
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

/* 鼠标点击特效 */
//var a_idx = 0;
jQuery(document).ready(function($) {
    $("main").click(function(e) {
        var a = new Array("Java", "Python", "C++", "C#", "C", "PHP",
            "JavaScript", "Perl", "Ruby", "GO", "Shell", "Django",
            "Linux", "Django", "MySQL", "MongoDB", "Redis", "HTML",
            "CSS", "JQuery", "Servlet", "Hibernate", "Scrapy", "Struts2",
            "Spring", "SpringMVC", "Mybatis", "Dubbo", "Maven", "Flask", "Tensorflow", "Caffe");

        // 随机输出
        var a_idx = Math.floor(Math.random()*a.length+1);
        var $i = $("<span/>").text("😋 "+a[a_idx]);
        // 按顺序输出
        // a_idx = (a_idx + 1) % a.length;
        var x = e.pageX,
                y = e.pageY;
                $i.css({
                    "z-index": 999999999999999999999999999999999999999999999999999999999999999999999,
                    "top": y - 20,
                    "left": x,
                    "position": "absolute",
                    "font-weight": "bold",
                    "color": "#09b1b9"
                });
        $("body").append($i);
        $i.animate({
            "top": y - 180,
            "opacity": 0
            },
            1500, function() {
            $i.remove();
        });
    });
});

function secondToDate(second) {
    if (!second) {
        return 0
    }
    var time = new Array(0,0,0,0,0);
    if (second >= 365 * 24 * 3600) {
        time[0] = parseInt(second / (365 * 24 * 3600));
        second %= 365 * 24 * 3600
    }
    if (second >= 24 * 3600) {
        time[1] = parseInt(second / (24 * 3600));
        second %= 24 * 3600
    }
    if (second >= 3600) {
        time[2] = parseInt(second / 3600);
        second %= 3600
    }
    if (second >= 60) {
        time[3] = parseInt(second / 60);
        second %= 60
    }
    if (second > 0) {
        time[4] = second
    }
    return time
}
function formatTime() {
    var create_time = Math.round(new Date(Date.UTC(2018, 05, 01, 0, 0, 0)).getTime() / 1000);
    var timestamp = Math.round((new Date().getTime() + 8 * 60 * 60 * 1000) / 1000);
    currentTime = secondToDate((timestamp - create_time));
    // currentTimeHtml = currentTime[0] + "年" + currentTime[1] + "天" + currentTime[2] + "时" + currentTime[3] + "分" + currentTime[4] + "秒";
    currentTimeHtml = currentTime[1] + "天" + currentTime[2] + "时" + currentTime[3] + "分" + currentTime[4] + "秒";
    document.getElementById("run_time").innerHTML = currentTimeHtml
}
