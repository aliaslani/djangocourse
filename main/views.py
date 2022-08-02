from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout, authenticate, login as auth_login
from django.contrib.auth.models import User, Group
from account.forms import CustomUserForm, TeacherForm, CourseForm, StudentForm, TeacherEditForm, CustomUserFormTeacher, CustomUserFormStudent
from django.contrib import messages
from account.models import Student, Teacher, Course, Mark
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from persiantools.jdatetime import JalaliDate
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
    form = TeacherEditForm(request.POST or None, initial={'address': teacher.address, 'phone': teacher.phone, 'degree': teacher.degree})
    if request.user.groups.filter(name='admin').exists():
        user_role = 'admin'
        if request.method == 'POST':
            if form.is_valid():
                teacher.phone = form.cleaned_data['phone']
                teacher.address = form.cleaned_data['address']
                teacher.degree = form.cleaned_data['degree']
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
        form1 = CustomUserFormTeacher(request.POST or None)
        form2 = TeacherForm(request.POST or None)
        if request.method == 'POST':
            if form1.is_valid():
                new_user = form1.save()
                new_user.save()
                new_user.groups.add(Group.objects.get(name='teacher'))
                messages.success(request, 'حساب کاربری با موفقیت ایجاد شد')
                if form2.is_valid():
                    new_teacher = Teacher.objects.create(user = new_user, phone=form2.cleaned_data['phone'], date_of_birth=JalaliDate(form2.cleaned_data['date_of_birth'].year, form2.cleaned_data['date_of_birth'].month, form2.cleaned_data['date_of_birth'].day ).to_gregorian(), address=form2.cleaned_data['address'], degree=form2.cleaned_data['degree'])
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
                course.start_date = JalaliDate(form.cleaned_data['start_date'].year, form.cleaned_data['start_date'].month, form.cleaned_data['start_date'].day ).to_gregorian()
                course.end_date = JalaliDate(form.cleaned_data['end_date'].year, form.cleaned_data['end_date'].month, form.cleaned_data['end_date'].day ).to_gregorian()
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
    student = Student.objects.get(id=student_id)
    form = StudentForm(request.POST or None, initial={'name': student.user.get_full_name, 'email': student.user.email, 'phone': student.phone, 'date_of_birth': JalaliDate.to_jalali(student.date_of_birth.year, student.date_of_birth.month, student.date_of_birth.day), 'courses': student.courses.all(), 'address': student.address, 'degree': student.degree})
    if request.user.groups.filter(name='admin').exists():
        user_role = 'admin'
        if request.method == 'POST':
            if form.is_valid():
                student.phone = form.cleaned_data['phone']
                student.address = form.cleaned_data['address']
                student.courses.set(form.cleaned_data['courses'])
                student.degree = form.cleaned_data['degree']
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
        form1 = CustomUserFormStudent(request.POST or None)
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

@login_required
def course_detail(request, course_id):
    if request.user.groups.filter(name='admin').exists():
        user_role = 'admin'
        course = Course.objects.get(id=course_id)
        return render(request, 'main/course_detail.html', {'course': course, 'user_role': user_role})
    else:
        return redirect('main:not_found')


@login_required
def student_detail(request, student_id):
    if request.user.groups.filter(name='admin').exists():
        user_role = 'admin'
        student = get_object_or_404(Student, id=student_id)
        courses = student.courses.all()
        return render(request, 'main/student_detail.html', {'student': student, 'user_role': user_role, 'courses': courses})
    else:
        return redirect('main:not_found')

@login_required
def teacher_detail(request, teacher_id):
    if request.user.groups.filter(name='admin').exists():
        user_role = 'admin'
        teacher = get_object_or_404(Teacher, id=teacher_id)
        courses = Course.objects.filter(teacher=teacher)
        return render(request, 'main/teacher_detail.html', {'teacher': teacher, 'user_role': user_role, 'courses': courses})
    else:
        return redirect('main:not_found')