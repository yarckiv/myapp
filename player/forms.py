from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import Music, UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput())


class RoomAdd(forms.Form):
    room_num = forms.CharField(label='# room')


class MusicFormAdd(forms.ModelForm):
    class Meta:
        model = Music
        fields = ['title', 'link']


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = ('username', 'password', 'room',)

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label='Password')

    class Meta:
        model = UserProfile
        fields = '__all__'

    def clean_password(self):
        return self.initial["password"]


