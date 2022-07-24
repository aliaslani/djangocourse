from django.forms import ModelForm
from django import forms
from account.models import Teacher, Course, Student
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CustomUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'first_name', 'last_name']

