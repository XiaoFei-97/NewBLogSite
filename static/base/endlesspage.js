 <!--<script>-->
        <!--/*endlesspage.js*/-->
        <!--var i = 1; //设置当前页数，全局变量-->
        <!--$(function () {-->
          <!--//根据页数读取数据-->
            <!--function getData(pagenumber) {-->
                <!--i++; //页码自动增加，保证下次调用时为新的一页。-->
                <!--// $.get("/blog_ajax", { pagenumber: pagenumber }, function (data) {-->
                <!--//   if (data.length > 0) {-->
                <!--//     var jsonObj = JSON.parse(data);-->
                <!--//     insertDiv(jsonObj);-->
                <!--//   }-->
                <!--// });-->
                <!--$.ajax({-->
                    <!--type: "POST",-->
                    <!--url: "/ajax_blog",-->
                    <!--data: { pagenumber: pagenumber },-->
                    <!--dataType: "json",-->
                    <!--success: function (data) {-->
                        <!--$(".loaddiv").hide();-->
                        <!--if (data.length > 0) {-->
                        <!--var jsonObj = JSON.parse(data);-->
                        <!--insertDiv(jsonObj);-->
                    <!--}-->
                    <!--},-->
                    <!--beforeSend: function () {-->
                        <!--$(".loaddiv").show();-->
                    <!--},-->
                    <!--error: function () {-->
                        <!--$(".loaddiv").hide();-->
                    <!--}-->
                <!--});-->
            <!--}-->
            <!--//初始化加载第一页数据-->
            <!--getData(1);-->
            <!--//生成数据html,append到div中-->
            <!--function insertDiv(json) {-->
                <!--var $mainDiv = $("#bloglist");-->
                <!--var html = '';-->
                <!--for (var i = 0; i < json.length; i++) {-->
                    <!--html += '<li>' + '<h2>' + '<a class="hvr-rotate"' + ' href="/detail/11" target="_Blank">' + json[i].id +-->
                        <!--'</a></h2><i><a href="/detail/11">' +-->
                        <!--'<img class="hvr-grow-shadow" src="图片" title="标题"></a></i><p class="blogtext">博客</p><p class="bloginfo">' +-->
                        <!--'<span>2018年12月22日</span><span><a class="hvr-wobble-vertical" href="分类">分类</a></span> <span>浏览(41）</span>' +-->
                        <!--'<span style="padding-left: 0px"><samp class="fa fa-comment"></samp>评论</span>' +-->
                        <!--'</p><a href="/detail/11" target="_blank" class="viewmore hvr-sweep-to-top">阅读原文</a></li>'-->

                <!--}-->
                <!--$mainDiv.append(html);-->
              <!--}-->
            <!--//==============核心代码=============-->
            <!--var winH = $(window).height(); //页面可视区域高度-->
            <!--var scrollHandler = function () {-->
            <!--var pageH = $(document.body).height();-->
            <!--var scrollT = $(window).scrollTop(); //滚动条top-->
            <!--var aa = (pageH - winH - scrollT) / winH;-->
            <!--if (aa < 0.02) {//0.02是个参数-->
                <!--if (i % 10 === 0) {//每10页做一次停顿！-->
                    <!--getData(i);-->
                    <!--$(window).unbind('scroll');-->
                    <!--$("#btn_Page").show();-->
                <!--} else {-->
                    <!--getData(i);-->
                    <!--$("#btn_Page").hide();-->
                <!--}-->
            <!--}-->
            <!--};-->
            <!--//定义鼠标滚动事件-->
            <!--$(window).scroll(scrollHandler);-->
            <!--//==============核心代码=============-->
            <!--//继续加载按钮事件-->
            <!--$("#btn_Page").click(function () {-->
                <!--getData(i);-->
                <!--$(window).scroll(scrollHandler);-->
           <!--});-->
        <!--});-->
    <!--</script>-->