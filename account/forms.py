from django.forms import ModelForm
from django import forms
from account.models import Teacher, Course, Student
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CustomUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'first_name', 'last_name']
    username = forms.CharField(label='نام کاربری', max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='کلمه عبور', max_length=30, required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='تکرار کلمه عبور', max_length=30, required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='ایمیل', max_length=30, required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label='نام', max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='نام خانوادگی', max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    roles_choices = (
        ('student', 'دانشجو'),
        ('teacher', 'استاد'),
    )
    role = forms.ChoiceField(label='نقش', choices=roles_choices, required=True, widget=forms.Select(attrs={'class': 'form-control'}))

    def username_validator(self, username):
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('نام کاربری تکراری است')
    
    def email_validator(self, email):
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('ایمیل تکراری است')

class TeacherForm(ModelForm):
    class Meta:
        model = Teacher
        fields = ['phone', 'address', 'date_of_birth', 'degree']
    phone = forms.CharField(label='شماره تلفن', widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(label='آدرس', widget=forms.TextInput(attrs={'class': 'form-control'}))
    date_of_birth = forms.DateField(label='تاریخ تولد', widget=forms.DateInput(attrs={'class': 'form-control'}))
    degree_choices = (
        ('دیپلم', 'دیپلم'),
        ('فوق دیپلم', 'فوق دیپلم'),
        ('لیسانس', 'لیسانس'),
        ('فوق لیسانس', 'فوق لیسانس'),
        ('دکتری', 'دکتری'),
    )
    degree = forms.ChoiceField(label='مدرک تحصیلی', choices=degree_choices, widget=forms.Select(attrs={'class': 'form-control'}))
    
class TeacherEditForm(ModelForm):
    class Meta:
        model = Teacher
        fields = ['phone', 'address', 'degree']
    phone = forms.CharField(label='شماره تلفن', widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(label='آدرس', widget=forms.TextInput(attrs={'class': 'form-control'}))
    degree_choices = (
        ('دیپلم', 'دیپلم'),
        ('فوق دیپلم', 'فوق دیپلم'),
        ('لیسانس', 'لیسانس'),
        ('فوق لیسانس', 'فوق لیسانس'),
        ('دکتری', 'دکتری'),
    )
    degree = forms.ChoiceField(label='مدرک تحصیلی', choices=degree_choices, widget=forms.Select(attrs={'class': 'form-control'}))


class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'start_date', 'end_date', 'length', 'teacher', 'status']
    name = forms.CharField(label='نام درس', max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    start_date = forms.DateField(label='تاریخ شروع', widget=forms.DateInput(attrs={'class': 'form-control'}))
    end_date = forms.DateField(label='تاریخ پایان', widget=forms.DateInput(attrs={'class': 'form-control'}))
    length = forms.IntegerField(label='طول درس', widget=forms.TextInput(attrs={'class': 'form-control'}))
    teacher = forms.ModelChoiceField(label='استاد', queryset=Teacher.objects.all(), required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    status_choices = (
        ('1', 'در حال برگزاری'),
        ('2', 'برگزار شده'),
        ('3', 'پایان داده شده'),
    )
    status = forms.ChoiceField(label='وضعیت', choices=status_choices, required=True, widget=forms.Select(attrs={'class': 'form-control'}))


class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = ['phone', 'date_of_birth', 'address', 'courses']
    phone = forms.CharField(label='شماره تلفن', widget=forms.TextInput(attrs={'class': 'form-control'}))
    date_of_birth = forms.DateField(label='تاریخ تولد', widget=forms.DateInput(attrs={'class': 'form-control'}))
    address = forms.CharField(label='آدرس', widget=forms.TextInput(attrs={'class': 'form-control'}))
    courses = forms.ModelMultipleChoiceField(label='دروس', queryset=Course.objects.all(), required=True, widget=forms.SelectMultiple(attrs={'class': 'form-control'}))
    degree_choices = (
        ('دیپلم', 'دیپلم'),
        ('فوق دیپلم', 'فوق دیپلم'),
        ('لیسانس', 'لیسانس'),
        ('فوق لیسانس', 'فوق لیسانس'),
        ('دکتری', 'دکتری'),
    )
    degree = forms.ChoiceField(label='مدرک تحصیلی', choices=degree_choices, widget=forms.Select(attrs={'class': 'form-control'}))


