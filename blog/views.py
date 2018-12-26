from django.shortcuts import get_object_or_404, render
from .models import Post, Category  # ReadNum
from django.core.paginator import *   # 导入分页功能
from django.conf import settings   # 导入settings,可以使用其中自定义的全局变量
# contenttypes 是Django内置的一个应用，可以追踪项目中所有app和model的对应关系，并记录在ContentType表中
from user.forms import *  # 导入登录模态框表单
from .tasks import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def home(request):
    """
    作用:网站首页的视图处理
    :param request: 请求对象
    :return: 首页模板视图
    """
    # 所有分类
    category_list = Category.objects.filter(status=0)

    # 所有博客列表
    # post_list = Post.objects.filter(Q(display=0) | Q(display__isnull=True))
    post_list = cache.get('post_list')
    if post_list is None:
        post_list = Post.objects.filter(Q(display=0) | Q(display__isnull=True)).filter(category__status=0)
        # 60*60表示60秒*60,也就是1小时
        cache.set('post_list', post_list, 30 * 60)

    # 最新发表的15篇博客
    # new_publish = Post.objects.filter(Q(display=0) | Q(display__isnull=True))[:15]
    new_publish = cache.get('new_publish')
    if new_publish is None:
        new_publish = Post.objects.filter(Q(display=0) | Q(display__isnull=True)).filter(category__status=0)[:15]
        # 60*60表示60秒*60,也就是1小时
        cache.set('new_publish', new_publish, 30 * 60)

    # 获取Post模型类或模型的实例，并返回ContentType表示该模型的实例
    post_content_type = ContentType.objects.get_for_model(Post)

    # 最新推荐的15篇博客
    # new_recommend = get_new_recommend_post(post_content_type)
    new_recommend = cache.get('new_recommend')
    if new_recommend is None:
        new_recommend = get_new_recommend_post(post_content_type)
        # 60*60表示60秒*60,也就是1小时
        cache.set('new_recommend', new_recommend, 30 * 60)

    # 随机推荐的15篇博客
    random_recommend = get_random_recomment()

    # 使用自定义的utils工具包get_seven_days_read_data,取出七天内每天的阅读计数总和
    # seven_dates, seven_read_nums = get_seven_days_read_data(post_content_type)

    # 使用自定义的utils工具包get_year_read_data,取出当年每月的阅读计数总和
    # thirty_dates, thirty_read_nums, year = get_year_read_data(post_content_type)

    # 阅读量周榜博客榜单
    # last_7_days_hot_data = get_7_days_read_posts()
    last_7_days_hot_data = cache.get('last_7_days_hot_data')
    if last_7_days_hot_data is None:
        last_7_days_hot_data = get_7_days_read_posts()
        # 60*60表示60秒*60,也就是1小时
        cache.set('last_7_days_hot_data', last_7_days_hot_data, 30 * 60)

    # 阅读量月榜博客榜单
    # last_30_days_hot_data = get_30_days_read_posts()
    last_30_days_hot_data = cache.get('last_30_days_hot_data')
    if last_30_days_hot_data is None:
        last_30_days_hot_data = get_30_days_read_posts()
        # 60*60表示60秒*60,也就是1小时
        cache.set('last_30_days_hot_data', last_30_days_hot_data, 30 * 60)

    # 阅读量总榜博客榜单
    # all_hot_posts = get_all_read_posts()
    all_hot_posts = cache.get('all_hot_posts')
    if all_hot_posts is None:
        all_hot_posts = get_all_read_posts()
        # 60*60表示60秒*60,也就是1小时
        cache.set('all_hot_posts', all_hot_posts, 30 * 60)

    # context用来渲染模板
    context = {
        'category_list': category_list, 'post_count': post_list.count,
        'new_publish': new_publish, 'new_recommend': new_recommend,
        'random_recommend': random_recommend,
        # 'seven_dates': seven_dates,'seven_read_nums': seven_read_nums, 'thirty_dates': thirty_dates,
        # 'thirty_read_nums': thirty_read_nums, 'year': str(year),
        'last_7_days_hot_data': last_7_days_hot_data, 'last_30_days_hot_data': last_30_days_hot_data,
        'all_hot_posts': all_hot_posts, 'LoginModalForm': LoginModalForm(), "RegModalForm": RegModalForm(),
        'ForgotPasswordModalForm': ForgotPasswordModalForm(),
        # 'today_hot_data': today_hot_data,
    }
    return render(request, 'home.html', context)


def get_blog_list_common_data(request, post_all_list):
    """
    博客列表,分类列表,时间排序列表的公共分页代码
    :param request: 请求对象
    :param post_all_list: 经过处理后的博客列表
    :return: 公共的context参数
    """
    # 创建一个分页器对象,参数分别是文章列表,每页最大文章数量
    # 这里的EACH_RAGE_BLOG_NUMBER等于10,已经当成常量写进了seetings里
    paginator = Paginator(post_all_list, settings.EACH_RAGE_BLOG_NUMBER)

    # 采用get方式获取用户访问的页码,如果获取不到,默认为第一页
    page_num = request.GET.get('page', 1)

    # 因为用户输入不一定是数字,所以需要用int(page_num),而django里的get_page会自动识别用户输入以及页码范围
    # 注意这里的page_of_list是一个paginator对象
    page_of_list = paginator.page(int(page_num))

    # 获取当前页码
    current_page_num = page_of_list.number

    # page_range = [current_page_num - 2, current_page_num - 1,
    # current_page_num, current_page_num + 1, current_page_num + 2]

    # 获取当前页码前后各两页的页码范围
    # 需要注意判断的是:如果当前页是第一页,那么前两页不能是0,也不能是-1,所以要使用内置max函数来与1比较最大值
    # 同理:如果当前页已经是最后一页,那么就不能取到当前页+2的页码了,所以要使用内置min函数来与最大页码比较最小值
    page_range = list(range(max(current_page_num - 2, 1), current_page_num)) + \
                 list(range(current_page_num, min(current_page_num + 2, paginator.num_pages) + 1))

    # 加上省略页码标记
    # paginator.num_pages表示一共有多少页码
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')

    # 加上首页尾页
    # paginator.num_pages表示一共有多少页码
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    # 所有博客的列表,且按时间越早创建越靠后排
    # post_list = Post.objects.all().order_by('-created_time')

    # count()是延伸下来的方法,用于计算总博客的数量
    # post_count = Post.objects.all().count()

    # 获取所有的分类
    category_list = Category.objects.filter(status=0)

    # 获取博客分类对应的博客数量
    # 给每个category对象绑定post_count字段
    post_category_list = []
    for category in category_list:
        category.post_count = Post.objects.filter(Q(display=0) | Q(display__isnull=True), category=category).count()
        post_category_list.append(category)

    # 获取博客的创建时间,且按创建时间月份排序
    # post_dates = Post.objects.dates('created_time', 'month', order='DESC')
    post_dates = cache.get('post_dates')
    if post_dates is None:
        post_dates = Post.objects.filter(category__status=0).dates('created_time', 'month', order='DESC')
        # 60*60表示60秒*60,也就是1小时
        cache.set('post_dates', post_dates, 30 * 60)

    # 获取日期归档对应的博客数量
    # 利用字典
    post_date_dict = {}
    for post_date in post_dates:
        post_date_count = Post.objects.filter(Q(display=0) | Q(display__isnull=True), category__status=0, created_time__year=post_date.year, created_time__month=post_date.month).count()
        post_date_dict[post_date] = post_date_count

    # 随机推荐的15篇博客
    random_recommend = get_random_recomment()

    # 最新推荐的15篇博客
    post_content_type = ContentType.objects.get_for_model(Post)
    # new_recommend = get_new_recommend_post(post_content_type)
    new_recommend = cache.get('new_recommend')
    if new_recommend is None:
        new_recommend = get_new_recommend_post(post_content_type)
        # 60*60表示60秒*60,也就是1小时
        cache.set('new_recommend', new_recommend, 30*60)

    # 阅读量总榜博客榜单
    # all_hot_posts = get_all_read_posts()
    all_hot_posts = cache.get('all_hot_posts')
    if all_hot_posts is None:
        all_hot_posts = get_all_read_posts()
        # 60*60表示60秒*60,也就是1小时
        cache.set('all_hot_posts', all_hot_posts, 30 * 60)

    # context用来渲染模板
    context = {'post_list': page_of_list.object_list,
               'page_of_list': page_of_list,
               'category_list': category_list,
               'page_range': page_range,
               'post_dates': post_date_dict,
               'random_recommend': random_recommend,
               'new_recommend': new_recommend,
               'all_hot_posts': all_hot_posts,
               'LoginModalForm': LoginModalForm(),
               "RegModalForm": RegModalForm(),
               'ForgotPasswordModalForm': ForgotPasswordModalForm(),
               }
    return context


def blog(request):
    """
    博客列表的视图处理
    :param request: 请求对象
    :return: 博客列表视图
    """
    # post_all_list = Post.objects.all().filter(Q(display=0) | Q(display__isnull=True))
    post_list = cache.get('post_list')
    if post_list is None:
        post_list = Post.objects.filter(Q(display=0) | Q(display__isnull=True)).filter(category__status=0)
        # 60*60表示60秒*60,也就是1小时
        cache.set('post_list', post_list, 30 * 60)

    # 使用公共的get_blog_list_common_data的方法
    context = get_blog_list_common_data(request, post_list)

    # 给request返回一个blog.html文件
    return render(request, 'blog/blog.html', context)


@csrf_exempt
def ajax_blog(request):
    """
    ajax加载博客内容
    :param request:
    :return: 博客json数据
    """

    # 采用get方式获取用户访问的页码,如果获取不到,默认为第一页
    page_num = request.POST.get('pagenumber', 1)
    print(page_num)
    post_list = cache.get('post_list')
    if post_list is None:
        post_list = Post.objects.filter(Q(display=0) | Q(display__isnull=True)).filter(category__status=0)
        # 60*60表示60秒*60,也就是1小时
        cache.set('post_list', post_list, 30 * 60)

        # 创建一个分页器对象,参数分别是文章列表,每页最大文章数量
        # 这里的EACH_RAGE_BLOG_NUMBER等于10,已经当成常量写进了seetings里
    paginator = Paginator(post_list, settings.EACH_RAGE_BLOG_NUMBER)

    # 因为用户输入不一定是数字,所以需要用int(page_num),而django里的get_page会自动识别用户输入以及页码范围
    # 注意这里的page_of_list是一个paginator对象
    page_of_list = paginator.page(int(page_num))
    posts = []
    for post in page_of_list.object_list:
        data = {
            'id': post.id,
            'title': post.title,
            'body': post.body,
            'created_time': post.created_time,
            'category': post.category.name,
            'pimage': post.pimage.name,
        }
        posts.append(data)
    return JsonResponse(posts, safe=False)


def detail(request, pk):
    """
    显示当前选择文章内容
    :param request: 请求对象
    :param pk: 每篇文章的pk值
    :return: 博客详情页视图
    """
    # 接收了一个pk值,这个值是在url中传递的主键,利用该主键可以找到文章的对象
    # get_object_or_404的用法是(模型名,get方法)
    post = get_object_or_404(Post, pk=pk)
    # post_all_list = Post.objects.filter(Q(display=0) | Q(display__isnull=True))
    post_list = cache.get('post_list')
    if post_list is None:
        post_list = Post.objects.filter(Q(display=0) | Q(display__isnull=True)).filter(category__status=0)
        # 60*60表示60秒*60,也就是1小时
        cache.set('post_list', post_list, 30 * 60)

    # 使用公共的get_blog_list_common_data的方法
    context = get_blog_list_common_data(request, post_list)

    # read_statistics_once_read是在read_statistics应用中的方法,表示计数+1
    read_cookie_key = read_statistics_once_read(request, post)

    # post_content_type = ContentType.objects.get_for_model(Post)
    # comments = Comment.objects.filter(content_type=post_content_type, object_id=post.pk, parent=None)

    # 在django中不能使用>=或<=,所以django自定义了__gt和__lt
    # 目的:得出创建时间比当前博客创建时间较晚的所有博客列表的最后一篇博客,也就是当前博客的上一篇
    # 因为博客是按照创建时间的先后来排序的:即先创建的靠后,那么上一篇博客创建时间晚于当前博客
    previous_post = Post.objects.filter(created_time__gt=post.created_time, display=0).filter(category__status=0).last()

    # 目的:得出创建时间比当前博客创建时间较早的所有博客列表的第一篇博客,也就是当前博客的下一篇
    # 因为博客是按照创建时间的先后来排序的:即先创建的靠后,那么上一篇博客创建时间早于当前博客
    next_post = Post.objects.filter(created_time__lt=post.created_time, display=0).filter(category__status=0).first()

    context.update({'article': post.body, 'title': post.title,
                    'author': post.author, 'created_time': post.created_time,
                    'category': post.category, 'previous_post': previous_post,
                    'next_post': next_post, 'read_num': post.get_read_num,
                    'user': request.user, 'post_id': post.id, 'post': post,
                    'LoginModalForm': LoginModalForm(),
                    # 'comments': comments.order_by('-comment_time'),
                    # 'comment_form': CommentForm(initial={
                    #   'content_type': post_content_type.model, 'object_id': pk, 'reply_comment_id': 0}),
                    # 'comment_count':Comment.objects.filter(content_type=post_content_type, object_id=post.pk).count()
               })
    response = render(request, 'blog/detail.html', context)

    # 第一个参数是键,键值,和过期时间
    response.set_cookie(read_cookie_key, 'True', domain="jzfblog.com", secure=True, httponly=True)  # 阅读cookie标记
    return response


def category(request, pk):
    """
    显示某分类下的全部文章
    :param request: 请求对象
    :param pk: 分类的主键值
    :return: 分类列表的视图
    """
    category = get_object_or_404(Category, pk=pk)

    # 因为从url中获得了一个category的pk,就可以在post中进行过滤
    post_list = Post.objects.filter(Q(display=0) | Q(display__isnull=True), category=category)

    date_list = cache.get('date_list')
    if date_list is None:
        date_list = Post.objects.filter(category__status=0).dates('created_time', 'month', order='DESC')
        # 60*60表示60秒*60,也就是1小时
        cache.set('date_list', date_list, 30 * 60)

    post_count = Post.objects.filter(Q(display=0) | Q(display__isnull=True), category__status=0).count()

    # 使用公共部分的 get_blog_list_common_data方法
    context = get_blog_list_common_data(request, post_list)

    # 新增了一个当前分类名称的键
    context.update({'category_name': category.name, 'date_list': date_list, 'post_count': post_count})

    # 给request返回一个category.html文件
    return render(request, 'blog/category.html', context)


def date(request, year, month):
    """
    显示某归档下的全部文章
    :param request: 请求对象
    :param year: 年
    :param month: 月
    :return: 归档的视图
    """
    # django比较坑的地方就是使用mysql存储数据时，因为时区的问题无法得到Asia/Shanghai的时间，即无法过滤出月份
    # 在这里采用的方法是先将月份转化为字符串的形式，然后再使用，发现可行
    month = str(month)

    post_list = Post.objects.all().filter(
        Q(display=0) | Q(display__isnull=True), created_time__year=year, created_time__month=month, category__status=0)
    # 将年月拼接一下
    post_time = year+'年'+month+'月'

    date_list = cache.get('date_list')
    if date_list is None:
        date_list = Post.objects.dates('created_time', 'month', order='DESC').filter(category__status=0)
        # 60*60表示60秒*60,也就是1小时
        cache.set('date_list', date_list, 30 * 60)

    post_count = Post.objects.filter(Q(display=0) | Q(display__isnull=True)).filter(category__status=0).count()

    context = get_blog_list_common_data(request, post_list)
    context.update({'post_time': post_time, 'date_list': date_list, 'post_count': post_count})

    return render(request, 'blog/date.html', context)


def page_not_found(request):
    """
    404错误视图
    :param request:
    :return: 404视图
    """
    return render(request, '404.html')


def looking(request):
    """
    搜索关键字标题
    :param request:
    :return:
    """
    wd = request.GET.get('wq', '')

    list = Post.objects.filter(Q(display=0) | Q(display__isnull=True)).filter(category__status=0, title__icontains=wd)

    # 使用公共的get_blog_list_common_data的方法
    context = get_blog_list_common_data(request, list)
    # 给request返回一个blog.html文件
    return render(request, 'blog/search.html', context)


# 错误：CSRF token missing or incorrect.
@csrf_exempt
def findWords(request):
    """
    查询数据库的文章标题
    :param request:
    :return:
    """
    key = request.POST.get('key', '')
    # print(key)
    # list = Post.objects.filter(Q(display=0) | Q(display__isnull=True), title__istartswith=key)[:2]
    list = Post.objects.filter(Q(display=0) | Q(display__isnull=True), title__icontains=key).filter(category__status=0)[:5]

    search_list = []
    for post in list:
        data = {
            'id': post.id,
            'title': post.title
        }
        search_list.append(data)
    # print(search_list)
    # 错误In order to allow non-dict objects to be serialized
    return JsonResponse(search_list, safe=False)

