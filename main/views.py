from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout, authenticate, login as auth_login
from django.contrib.auth.models import User, Group
from account.forms import CustomUserForm, TeacherForm, CourseForm, StudentForm
from django.contrib import messages
from account.models import Student, Teacher, Course, Mark
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
# Create your views here.

def index(request):
    user = request.user
    marks = []
    students = []
    teachers = []
    courses = []
    if user.is_authenticated:
        if user.groups.filter(name='admin').exists():
            user_role = 'admin'
            courses = Course.objects.all()
            students = Student.objects.all()
            teachers = Teacher.objects.all()
        elif user.groups.filter(name='teacher').exists():
            user_role = 'teacher'
            courses = Course.objects.filter(teacher=user.teacher).all()
        elif user.groups.filter(name='student').exists():
            user_role = 'student'
            courses = Student.objects.get(user=user).courses.all()
            marks = Mark.objects.filter(student=Student.objects.get(user=user))
        
        
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
def students(request):
    if request.user.groups.filter(name='admin').exists():
        user_role = 'admin'
        students = Student.objects.all()
        return render(request, 'main/students.html', {'students': students, 'user_role': user_role})
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

@login_required
def teacher_edit(request, teacher_id):
    teacher = Teacher.objects.get(id=teacher_id)
    form = TeacherForm(request.POST or None, initial={'name': teacher.name, 'email': teacher.email, 'phone': teacher.phone, 'age': teacher.age, 'experieces': teacher.experieces})
    if request.user.groups.filter(name='admin').exists():
        user_role = 'admin'
        if request.method == 'POST':
            if form.is_valid():
                teacher.name = form.cleaned_data['name']
                teacher.email = form.cleaned_data['email']
                teacher.phone = form.cleaned_data['phone']
                teacher.age = form.cleaned_data['age']
                teacher.experieces = form.cleaned_data['experieces']
                teacher.save()
                return redirect('main:teachers')
        return render(request, 'main/teacher_edit.html', {'teacher': teacher, 'user_role': user_role, 'form': form})
    else:
        return redirect('main:not_found')

@login_required
def teacher_delete(request, teacher_id):
    if request.user.groups.filter(name='admin').exists():
        user_role = 'admin'
        teacher = Teacher.objects.get(id=teacher_id)
        teacher.delete()
        teacher.save()
        return redirect('main:teachers')
    else:
        return redirect('main:not_found')

@login_required
def teacher_add(request):
    if request.user.groups.filter(name='admin').exists():
        user_role = 'admin'
        form1 = CustomUserForm(request.POST or None)
        form2 = TeacherForm(request.POST or None)
        if request.method == 'POST':
            if form1.is_valid():
                new_user = form1.save()
                new_user.save()
                new_user.groups.add(Group.objects.get(name='teacher'))
                messages.success(request, 'حساب کاربری با موفقیت ایجاد شد')
                if form2.is_valid():
                    new_teacher = Teacher.objects.create(user = new_user, phone=form2.cleaned_data['phone'], date_of_birth=form2.cleaned_data['date_of_birth'], address=form2.cleaned_data['address'], degree=form2.cleaned_data['degree'])
                    new_teacher.save()
                    messages.success(request, 'استاد جدید با موفقیت ایجاد شد')
                    return redirect('main:teachers')
        return render(request, 'main/teacher_add.html', {'form1': form1, 'form2':form2, 'user_role': user_role})
    else:
        return redirect('main:not_found')

def user_add(request):
    if request.user.groups.filter(name='admin').exists():
        user_role = 'admin'
        form = CustomUserForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                user = User.objects.get(username=form.cleaned_data['username'])
                user.groups.add(Group.objects.get(name=form.cleaned_data['role']))
                user.save()
                messages.success(request, 'حساب کاربری جدید با موفقیت ایجاد شد')
                return redirect('main:users')
        return render(request, 'main/user_add.html', {'form': form, 'user_role': user_role})
    else:
        return redirect('main:not_found')

@login_required
def course_add(request):
    if request.user.groups.filter(name='admin').exists():
        user_role = 'admin'
        form = CourseForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, 'درس جدید با موفقیت افزوده شد')
                return redirect('main:courses')
        return render(request, 'main/course_add.html', {'form': form, 'user_role': user_role})
    else:
        return redirect('main:not_found')

@login_required
def course_edit(request, course_id):
    course = Course.objects.get(id=course_id)
    form = CourseForm(request.POST or None, initial={'name': course.name, 'length': course.length, 'teacher': course.teacher, 'status': course.status})
    if request.user.groups.filter(name='admin').exists():
        user_role = 'admin'
        if request.method == 'POST':
            if form.is_valid():
                course.name = form.cleaned_data['name']
                course.length = form.cleaned_data['length']
                course.teacher = form.cleaned_data['teacher']
                course.status = form.cleaned_data['status']
                course.save()
                return redirect('main:courses')
        return render(request, 'main/course_edit.html', {'course': course, 'user_role': user_role, 'form': form})
    else:
        return redirect('main:not_found')

@login_required
def course_delete(request, course_id):
    if request.user.groups.filter(name='admin').exists():
        course = get_object_or_404(Course, id=course_id)
        course.delete()
        return redirect('main:courses')
    else:
        return redirect('main:not_found')


@login_required
def student_edit(request, student_id):
    student = student.objects.get(id=student_id)
    form = StudentForm(request.POST or None, initial={'name': student.name, 'email': student.email, 'phone': student.phone, 'age': student.age, 'courses': student.courses.all()})
    if request.user.groups.filter(name='admin').exists():
        user_role = 'admin'
        if request.method == 'POST':
            if form.is_valid():
                student.name = form.cleaned_data['name']
                student.email = form.cleaned_data['email']
                student.phone = form.cleaned_data['phone']
                student.age = form.cleaned_data['age']
                student.experieces = form.cleaned_data['experieces']
                student.save()
                return redirect('main:students')
        return render(request, 'main/student_edit.html', {'student': student, 'user_role': user_role, 'form': form})
    else:
        return redirect('main:not_found')

@login_required
def student_delete(request, student_id):
    if request.user.groups.filter(name='admin').exists():
        user_role = 'admin'
        student = student.objects.get(id=student_id)
        student.delete()
        student.save()
        return redirect('main:students')
    else:
        return redirect('main:not_found')

@login_required
def student_add(request):
    if request.user.groups.filter(name='admin').exists():
        user_role = 'admin'
        form1 = CustomUserForm(request.POST or None)
        form2 = StudentForm(request.POST or None)
        if request.method == 'POST':
            if form1.is_valid():
                new_user = form1.save()
                new_user.save()
                new_user.groups.add(Group.objects.get(name='student'))
                messages.success(request, 'حساب کاربری با موفقیت ایجاد شد')
                if form2.is_valid():
                    new_student = Student.objects.create(user = new_user, phone=form2.cleaned_data['phone'], date_of_birth=form2.cleaned_data['date_of_birth'], address=form2.cleaned_data['address'],degree=form2.cleaned_data['degree'])
                    new_student.courses.set(form2.cleaned_data['courses'])
                    new_student.save()
                    messages.success(request, 'دانشجوی جدید با موفقیت افزوده شد')
                    return redirect('main:students')
        return render(request, 'main/student_add.html', {'form1': form1, 'form2':form2, 'user_role': user_role})
    else:
        return redirect('main:not_found')
