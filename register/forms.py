from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User #import User model so we can save it in user DB
from django import forms
from django.core.exceptions import ValidationError
from django import forms


class RegisterForm(UserCreationForm):
    """Class that inherits from UserCreationForm, thats why we can add additinal fields to it"""

    email_addr = forms.EmailField()
    #gender = forms.BooleanField()

    class Meta:
        model = User #model used is User
        fields = ["username", "email_addr", "password1", "password2"] #, 'gender'

