from django import forms

from apps.operation.models import UserFavorite

class UserFavoriteForm(forms.ModelForm):
    class Meta:
        model = UserFavorite
        fields = ['fav_id', 'fav_type']