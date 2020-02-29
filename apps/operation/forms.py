from django import forms

from apps.operation.models import UserFavorite, CourseComments

class CommentsForm(forms.ModelForm):
    class Meta:
        model = CourseComments
        fields = ['course', 'comments']

class UserFavoriteForm(forms.ModelForm):
    class Meta:
        model = UserFavorite
        fields = ['fav_id', 'fav_type']