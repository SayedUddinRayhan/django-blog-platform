from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        # fields = ['username', 'email', 'password1', 'password2']

        # user creation form use korle password1 and password2 automatically add hoye jay
        fields = ['username', 'email', 'first_name', 'last_name']

class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


