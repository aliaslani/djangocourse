from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout, authenticate, login as auth_login
from django.contrib.auth.models import User
from .forms import CustomUserForm
from django.contrib import messages
from .models import Student, Teacher, Course, Mark  

# Create your views here.






def register(request):
    if request.user.is_authenticated:
        return redirect ('main:index')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        user = User.objects.filter(username=username)
        if user:
            messages.error(request, 'نام کاربری تکراری است')
            return render(request, 'account/register.html')
        user = User.objects.filter(email=email)
        if user:
            messages.error(request, 'ایمیل تکراری است')
            return render(request, 'account/register.html')
        user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        user.save()
        messages.success(request, 'حساب کاربری با موفقیت ایجاد شد')
        return render(request, 'account/login.html')
    return render(request, 'account/register.html')

def login(request):
    if request.user.is_authenticated:
        return redirect ('account:index')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'شما با موفقیت وارد شدید')
            return render(request, 'main/index.html')
        else:
            messages.error(request, 'نام کاربری یا کلمه عبور اشتباه است')
    return render(request, 'account/login.html')

def logout_process(request):
    logout(request)
    messages.success(request, 'شما با موفقیت خارج شدید')
    return redirect('account:login')