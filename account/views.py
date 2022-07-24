from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout, authenticate, login as auth_login
from django.contrib.auth.models import User, Group
from .forms import CustomUserForm
from django.contrib import messages
from .models import Student, Teacher, Course, Mark  

# Create your views here.






def register(request):
    if request.user.is_authenticated:
        return redirect ('main:index')
    form = CustomUserForm()
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.groups.add(Group.objects.get(name=form.cleaned_data['role']))
            user.save()
            messages.success(request, 'شما با موفقیت ثبت نام کردید')
            return redirect('account:login')
    return render(request, 'account/register.html', {'form': form})

def login(request):
    if request.user.is_authenticated:
        return redirect ('account:index')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'شما با موفقیت وارد شدید')
            return redirect('main:index')
        else:
            messages.error(request, 'نام کاربری یا کلمه عبور اشتباه است')
    return render(request, 'account/login.html')

def logout_process(request):
    logout(request)
    messages.success(request, 'شما با موفقیت خارج شدید')
    return redirect('account:login')