from django import forms  # django表单功能
from django.contrib import auth
from django.contrib.auth.models import User


class LoginModalForm(forms.Form):
    """
    用户登录表单
    """
    # 用户名
    username_or_email = forms.CharField(label='帐号',
                                        widget=forms.TextInput(
                                            attrs={'class': 'form-control', 'placeholder': '请输入用户名或邮箱'}))

    # 密码
    password = forms.CharField(label='密码',
                               widget=forms.PasswordInput(
                                   attrs={'class': 'form-control', 'placeholder': '请输入密码'}))

    def clean(self):
        """
        清洗输入不合格的表单
        :return: 清洗后的数据
        """
        username_or_email = self.cleaned_data['username_or_email']
        password = self.cleaned_data['password']
        user = auth.authenticate(username=username_or_email, password=password)
        # 判断用户是否存在
        if user is None:
            if User.objects.filter(email=username_or_email).exists():
                username = User.objects.get(email=username_or_email).username
                user = auth.authenticate(username=username, password=password)
                if not user is None:
                    self.cleaned_data['user'] = user
                    return self.cleaned_data
                else:
                    raise forms.ValidationError('用户名或密码不正确,请重试')

            raise forms.ValidationError('用户名或密码不正确,请重试')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data


class RegModalForm(forms.Form):
    """
    用户注册表单
    """
    # 用户名
    username = forms.CharField(
        label='账号',
        max_length=20,
        min_length=3,
        widget=forms.TextInput(
           attrs={'class': 'form-control', 'placeholder': '请输入用户名'}))

    # 邮箱
    email = forms.EmailField(
        label='邮箱',
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': '请输入邮箱'}))

    # 密码
    password = forms.CharField(
        label='密码',
        min_length=6,
        widget=forms.PasswordInput(
           attrs={'class': 'form-control', 'placeholder': '请输入密码'}))

    # 再次输入密码
    # password_again = forms.CharField(
    #     label='密码',
    #     min_length=6,
    #     widget=forms.PasswordInput(
    #         attrs={'placeholder': '再输入一次密码'}))

    # 验证码
    verification_code = forms.CharField(
        label='验证码',
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '请在邮箱中查收'}
        )
    )

    def __init__(self, *args,  **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(RegModalForm, self).__init__(*args, **kwargs)

    # def clean_username(self):
    #     """
    #     清洗输入的用户名
    #     :return: 清洗后的用户名
    #     """
    #     username = self.cleaned_data['username']
    #     if User.objects.filter(username=username).exists():
    #         raise forms.ValidationError('用户名已存在')
    #     return username

    # def clean_email(self):
    #     """
    #     清洗输入的邮箱
    #     :return: 清洗后的邮箱
    #     """
    #     email = self.cleaned_data['email']
    #     if User.objects.filter(email=email).exists():
    #         raise forms.ValidationError('邮箱已存在')
    #     return email

    # def clean_verification_code(self):
    #     code = self.request.session.get('register_code', '').lower()
    #     verification_code = self.cleaned_data.get('verification_code', '').lower()
    #     if not (code != '' and code == verification_code):
    #         raise forms.ValidationError('验证码不正确')
    #     return self.cleaned_data

    # def clean_password_again(self):
    #     """
    #     清洗第二次输入的密码
    #     :return: 输入一致的密码
    #     """
    #     password = self.cleaned_data['password']
    #     password_again = self.cleaned_data['password_again']
    #
    #     if password != password_again:
    #         raise forms.ValidationError('两次输入的密码不一致')
    #     return password


class ChangeNameForm(forms.Form):
    new_nickname = forms.CharField(
        label='新昵称',
        max_length=20,
        min_length=3,
        widget=forms.TextInput(
            attrs={'placeholder': '请输入新的昵称'}
        )
    )

    def __init__(self, *args,  **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangeNameForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 验证用户是否处在登录状态
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户尚未登录')
        return self.cleaned_data

    def clean_new_nickname(self):
        new_nickname = self.cleaned_data.get('new_nickname', '').strip()
        if new_nickname == '':
            raise forms.ValidationError("新的昵称不能为空")
        return new_nickname


class ChangePasswordForm(forms.Form):

    past_password = forms.CharField(
        label='原密码',
        min_length=6,
        widget=forms.PasswordInput(
            attrs={'placeholder': '请输入原密码'}
        )
    )

    new_password = forms.CharField(
        label='新密码',
        min_length=6,
        widget=forms.PasswordInput(
            attrs={'placeholder': '请输入新密码'}
        )
    )

    # new_password_again = forms.CharField(
    #     label='新密码',
    #     min_length=6,
    #     widget=forms.PasswordInput(
    #         attrs={'placeholder': '再输入一次密码'}
    #     )
    # )

    def __init__(self, *args,  **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    # def clean(self):
    #     # 验证新密码是否一致
    #     new_password = self.cleaned_data.get('new_password', '')
    #     new_password_again = self.cleaned_data.get('new_password_again', '')
    #     if new_password != new_password_again or new_password == '':
    #         raise forms.ValidationError('两次输入密码不一致')
    #     return self.cleaned_data

    def clean_past_password(self):
        """验证原密码是否正确"""
        past_password = self.cleaned_data.get('past_password', '')
        if not self.user.check_password(past_password):
            raise forms.ValidationError('原密码不正确')
        return past_password


class BindEmailForm(forms.Form):
    email = forms.EmailField(
        label='邮箱',
        widget=forms.EmailInput(
            attrs={'placeholder': '请输入邮箱'}
        )
    )
    verification_code = forms.CharField(
        label='验证码',
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': '请在邮箱中查收'}
        )
    )

    def __init__(self, *args,  **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(BindEmailForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 验证用户是否处在登录状态
        if self.request.user.is_authenticated:
            self.cleaned_data['user'] = self.request.user
        else:
            raise forms.ValidationError('用户尚未登录')

        # 判断用户是否已绑定邮箱
        if self.request.user.email != '':
            raise forms.ValidationError('你已经绑定邮箱')

        # 判断验证码
        # code = self.request.session.get('bind_email_code', '')
        # verification_code = self.cleaned_data.get('verification_code', '')
        # if not (code != '' and code == verification_code):
        #     raise forms.ValidationError('验证码不正确')

        return self.cleaned_data

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('该邮箱已被绑定')
        return email

    def clean_verification_code(self):
        code = self.request.session.get('bind_eamil_code', '').lower()
        verification_code = self.cleaned_data.get('verification_code', '').lower()
        if not (code != '' and code == verification_code):
            raise forms.ValidationError('验证码不正确')
        return self.cleaned_data


class ForgotPasswordModalForm(forms.Form):
    # 邮箱
    password_email = forms.EmailField(
        label='邮箱',
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': '请输入绑定过的邮箱'}
        )
    )

    new_password = forms.CharField(
        label='密码',
        min_length=6,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': '请输入新密码'}
        )
    )

    # 验证码
    password_verification_code = forms.CharField(
        label='验证码',
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '请在邮箱中查收'}
        )
    )

    def __init__(self, *args,  **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(ForgotPasswordModalForm, self).__init__(*args, **kwargs)

    # def clean_email(self):
    #     email = self.cleaned_data['email'].strip()
    #
    #     if not User.objects.filter(email=email).exists():
    #         raise forms.ValidationError('邮箱不存在')
    #     return email
    #
    # def clean_password_verification_code(self):
    #     verification_code = self.cleaned_data.get('password_verification_code', '').strip()
    #     if verification_code == '':
    #         raise forms.ValidationError('验证码不能为空')
    #
    #     # 判断验证码
    #     code = self.request.session.get('forgot_password_code', '').lower()
    #     verification_code = self.cleaned_data.get('verification_code', '').lower()
    #     if not (code != '' and code == verification_code):
    #         raise forms.ValidationError('验证码不正确')
    #
    #     return verification_code


    def clean_new_password(self):
        new_password = self.cleaned_data.get('new_password', '')
        if new_password == '':
            raise forms.ValidationError('密码不能为空')
        return new_password

