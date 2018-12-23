from haystack import indexes
from haystack.views import SearchView
from read_statistics.utils import get_random_recomment, get_new_recommend_post, get_all_read_posts
from django.contrib.contenttypes.fields import ContentType
from .models import Post
from django.core.paginator import *   # 导入分页功能
from blogproject.settings import *
from user.forms import *


class PostIndex(indexes.SearchIndex, indexes.Indexable):
    # 创建文章索引类
    text = indexes.EdgeNgramField(document=True, use_template=True)

    def get_model(self):
        return Post

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class MySeachView(SearchView):
    """
    作用：自定义的search视图
    SearchView：继承SearchView类
    """
    def extra_context(self):  # 重载extra_context来添加额外的context内容
        """
        添加自定义的context参数，传递到search.html视图
        :return: 自定义的context参数
        """
        context = super(MySeachView, self).extra_context()

        # 这里的EACH_RAGE_BLOG_NUMBER等于10,已经当成常量写进了seetings里
        paginator = Paginator(self.results, EACH_RAGE_BLOG_NUMBER)

        # 采用get方式获取用户访问的页码,如果获取不到,默认为第一页
        page_num = self.request.GET.get('page', 1)

        # 因为用户输入不一定是数字,所以需要用int(page_num),而django里的get_page会自动识别用户输入以及页码范围
        # 注意这里的page_of_list是一个paginator对象
        page_of_list = paginator.page(int(page_num))

        key = self.request.GET.get('q')

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

        # 随机推荐的15篇博客
        random_recommend = get_random_recomment()

        # 最新推荐的15篇博客
        post_content_type = ContentType.objects.get_for_model(Post)
        new_recommend = get_new_recommend_post(post_content_type)

        # 阅读量总榜博客榜单
        all_hot_posts = get_all_read_posts()
        context = {
                'page_range': page_range,
                'random_recommend': random_recommend,
                'new_recommend': new_recommend,
                'all_hot_posts': all_hot_posts,
                'key': key,
                'LoginModalForm': LoginModalForm(),
                "RegModalForm": RegModalForm(),
                'ForgotPasswordModalForm': ForgotPasswordModalForm(),
            }
        return context
