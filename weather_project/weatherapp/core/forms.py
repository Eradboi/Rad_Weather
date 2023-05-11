from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class RegisterForm(UserCreationForm):
    email = forms.EmailField()
# the below is for saving the users input into their database the class must be (meta)
    class Meta:
        model = User
        # the fields is to define how the fields of the form would appear
        fields = ["username", "email", "password1", "password2"]