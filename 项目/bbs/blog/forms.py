from django import forms
from django.core.validators import RegexValidator


class LoginForm(forms.Form):

    user = forms.CharField(
        min_length=6,
        label='用户名',
        error_messages={
            "required": "用户名不能为空",
            "min_length": "用户名不能少于6位"
        },
        validators=[RegexValidator(r'[a-zA-Z][\w]+','用户名以英文字母开头'),],
        widget=forms.widgets.TextInput(
            attrs={'class':'form-control'}
        )
    )
    pwd = forms.CharField(
        label='密码',
        min_length=6,
        widget=forms.widgets.PasswordInput(
            attrs={'class': 'form-control'}
        ),
        error_messages={
            "required": "用户名不能为空",
            "min_length": "用户名不能少于6位"
        },
    )
