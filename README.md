##DjangoBlog
####此网站使用Django与Bootstrap

####使用方法:
下载到本地后，使用下面命令安装到环境中
```bash
pip install -r requirements.txt
```
运行代码
```bash
python manage.py runserver
```
-------------------
####注意事项：
>如出现Django导入出错，可能是因为在安装第三方包时，默认将Django卸载重新安装成了Django2.0的版本，因为我的项目中使用的是Django1.10.6，所以只需要重新安装Django1.10.6版本即可
```bash
pip install django==1.10.6
```
####部分代码展示
```python
class Category(models.Model):
    """
    Django 要求模型必须继承 models.Model 类。
    Category 只需要一个简单的分类名 name 就可以了。
    CharField 指定了分类名 name 的数据类型，CharField 是字符型，
    CharField 的 max_length 参数指定其最大长度，超过这个长度的分类名就不能被存入数据库。
    """
    name = models.CharField(max_length=20, verbose_name=u'分类')

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类'

    def __str__(self):

        return self.name
```
```python

class Tag(models.Model):
    """
    标签 Tag 也比较简单，和 Category 一样。
    再次强调一定要继承 models.Model 类！
    """
    name = models.CharField(max_length=100, verbose_name=u'标签')

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签'

    def __str__(self):

        return self.name
```
