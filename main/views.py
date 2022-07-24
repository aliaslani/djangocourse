from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout, authenticate, login as auth_login
from django.contrib.auth.models import User
from account.forms import CustomUserForm
from django.contrib import messages
from account.models import Student, Teacher, Course, Mark
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    user = request.user
    marks = []
    students = []
    teachers = []
    courses = []
    if user.is_authenticated:
        if user.groups.filter(name='student').exists():
            user_role = 'student'
            courses = Student.objects.get(user=user).courses.all()
            marks = Mark.objects.filter(student=Student.objects.get(user=user))
        elif user.groups.filter(name='teacher').exists():
            user_role = 'teacher'
            courses = Course.objects.filter(teacher=user.teacher).all()
        elif user.groups.filter(name='admin').exists():
            user_role = 'admin'
            courses = Course.objects.all()
            students = Student.objects.all()
            teachers = Teacher.objects.all()
        return render(request, 'main/index.html', {'courses': courses, 'marks': marks, 'students': students, 'teachers': teachers, 'user_role': user_role})
    return redirect('account:login')



def pricing(request):
    return render(request, 'main/pricing.html')

@login_required
def users(request):
    if request.user.groups.filter(name='admin').exists():
        user_role = 'admin'
        users = User.objects.all()
        return render(request, 'main/users.html', {'users': users, 'user_role': user_role})
    else:
        return redirect('main:not_found')

@login_required
def teachers(request):
    if request.user.groups.filter(name='admin').exists():
        user_role = 'admin'
        teachers = Teacher.objects.all()
        return render(request, 'main/teachers.html', {'teachers': teachers, 'user_role': user_role})
    else:
        return redirect('main:not_found')

@login_required
def courses(request):
    if request.user.groups.filter(name='admin').exists():
        user_role = 'admin'
        courses = Course.objects.all()
        return render(request, 'main/courses.html', {'courses': courses, 'user_role': user_role})
    else:
        return redirect('main:not_found')

def not_found(request):
    return render(request, 'main/404.html')