// 滚动动画
$(function () {
    $(window).scroll(function(){
        //开始监听滚动条
        //获取当前滚动条高度
        var top = $(document).scrollTop();
        var week_top = $("#week").offset().top;
        var month_top = $("#month").offset().top;
        var all_top = $("#all").offset().top;
        // 页面高度
        var height = $(window).height() - 50;
        //用于调试 弹出当前滚动条高度
        //alert(hot_height);

        //判断如果滚动条大于90则弹出 "ok"

        if(top > week_top - height ){

            //alert("ok");
            $('#week').addClass("fadeIn");
        }

        if(top > month_top - height ){
            $('#month').addClass("fadeIn");
        }
        if(top > all_top - height ){

            // alert("ok");
            $('#all').addClass("fadeIn");
        }

    })
});
