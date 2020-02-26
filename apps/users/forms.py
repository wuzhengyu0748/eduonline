from django import forms

from apps.users.models import UserProfile

class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)

class RegisterForm(forms.Form):
    mobile = forms.CharField(required=True, min_length=11, max_length=11)
    password = forms.CharField(required=True, min_length=6)

    def clean_mobile(self):
        mobile = self.data.get('mobile')
        users = UserProfile.objects.filter(mobile=mobile)
        if users:
            raise forms.ValidationError('该手机号已注册')
        return mobile