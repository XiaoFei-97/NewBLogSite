from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist
from ckeditor.widgets import CKEditorWidget
from DjangoUeditor.widgets import UEditorWidget
from .models import Comment


class CommentForm(forms.Form):
    """
    提交评论表单
    """
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    text = forms.CharField(widget=UEditorWidget(
        attrs={"width": 'auto', "height": 'auto',
               "toolbars": [['fullscreen', 'source', 'undo', 'redo', 'bold', 'italic',
                             'underline', 'fontborder', 'strikethrough', 'superscript',
                             'subscript', 'removeformat', 'formatmatch', 'autotypeset',
                             'blockquote', 'pasteplain', '|', 'forecolor', 'backcolor',
                             'insertorderedlist', 'insertunorderedlist','selectall',
                            'cleardoc', 'emotion']]}),
        error_messages={'required': '评论内容不能为空'})
    # text = forms.CharField(widget=CKEditorWidget(config_name='comment_ckeditor'),
    #                        error_messages={'required': '您尚未写任何评论内容'})

    reply_comment_id = forms.IntegerField(widget=forms.HiddenInput(attrs={'id': 'reply_comment_id'}))

    def __init__(self, *args,  **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(CommentForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 验证用户是否处在登录状态
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('您尚未登录，请先登录才能评论')

        # 评论对象验证
        content_type = self.cleaned_data['content_type']
        object_id = self.cleaned_data['object_id']
        # 找到post对象
        try:
            models_class = ContentType.objects.get(model=content_type).model_class()
            models_obj = models_class.objects.get(pk=object_id)
            self.cleaned_data['content_object'] = models_obj
        except ObjectDoesNotExist:
            raise forms.ValidationError('评论对象不存在')
        return self.cleaned_data

    def clean_reply_comment_id(self):
        reply_comment_id = self.cleaned_data['reply_comment_id']
        if reply_comment_id < 0:
            raise forms.ValidationError('回复出错')
        elif reply_comment_id == 0:
            self.cleaned_data['parent'] = None
        elif Comment.objects.filter(pk=reply_comment_id).exists():
            self.cleaned_data['parent'] = Comment.objects.get(pk=reply_comment_id)
        else:
            raise forms.ValidationError('回复出错')

        return reply_comment_id
