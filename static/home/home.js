$(function () {
    $('#read-nav li').click(function(){

        $(this).blur(); //消除焦点
        //alert($(this).index());

        $(this).addClass('active').siblings().removeClass('active');

        // $(this).index() 获取所在层级索引值
        // alert($(this).index());

        $('#contents #read-item').eq($(this).index()).addClass('cur').siblings().removeClass('cur');
        $('html').animate({scrollTop: $('#read-nav').offset().top - 110}, 500, function () {
         $('#read-nav').focus()
        });
    });
});