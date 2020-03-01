from django import forms

from apps.users.models import UserProfile

class ChangePwdForm(forms.Form):
    password1 = forms.CharField(required=True)
    password2 = forms.CharField(required=True)

    def clean(self):
        pwd1 = self.cleaned_data["password1"]
        pwd2 = self.cleaned_data["password2"]

        if pwd1 != pwd2:
            raise forms.ValidationError("两次输入密码不一致")
        return self.cleaned_data

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'gender', 'birthday', 'address']

class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['head_image']

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