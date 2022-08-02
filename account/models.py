from django.db import models
from datetime import datetime
from khayyam import JalaliDate
from persiantools import digits

# Create your models here.


class Teacher(models.Model):
    class Meta:
        verbose_name = 'استاد'
        verbose_name_plural = 'استاد'
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, verbose_name='کاربر')
    phone = models.CharField(max_length=11, verbose_name='شماره تلفن')
    date_of_birth = models.DateField('تاریخ تولد')
    address = models.CharField('آدرس', max_length=200)
    join_date = models.DateField('تاریخ عضویت', auto_now_add=True)
    
    degree_choices = (
        ('دیپلم', 'دیپلم'),
        ('فوق دیپلم', 'فوق دیپلم'),
        ('لیسانس', 'لیسانس'),
        ('فوق لیسانس', 'فوق لیسانس'),
        ('دکتری', 'دکتری'),
    )
    degree = models.CharField('مدرک', max_length=10, choices=degree_choices)

    def get_full_name(self):
        return self.user.first_name + ' ' + self.user.last_name

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

    def jjoin_date(self):
        return digits.en_to_fa(JalaliDate(self.join_date).strftime('%A %d %B %Y'))
    
    def jdate_of_birth(self):
        return digits.en_to_fa(JalaliDate(self.date_of_birth).strftime('%A %d %B %Y'))

class Course(models.Model):
    class Meta:
        verbose_name = 'دوره'
        verbose_name_plural = 'دوره '
    name = models.CharField(max_length=50, verbose_name='نام دوره')
    start_date = models.DateField('تاریخ شروع')
    end_date = models.DateField('تاریخ پایان')
    length = models.IntegerField(verbose_name='طول دوره')
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT, verbose_name='استاد')
    status_choices = (
        ('1', 'در حال برگزاری'),
        ('2', 'برگزار شده'),
        ('3', 'پایان داده شده'),
    )
    status = models.CharField(max_length=1, choices=status_choices, verbose_name='وضعیت')

    def get_time_difference_in_days(self):
        return (self.end_date - self.start_date).days
    
    def get_time_untill_now_in_days(self):
        return (datetime.now().date() - self.start_date).days

    def jstart_date(self):
        return digits.en_to_fa(JalaliDate(self.start_date).strftime('%A %d %B %Y'))
    def jend_date(self):
        return digits.en_to_fa(JalaliDate(self.end_date).strftime('%A %d %B %Y'))
    
    def __str__(self):
        return self.name

class Student(models.Model):
    class Meta:
        verbose_name = 'دانشجو'
        verbose_name_plural = 'دانشجو'
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='student', verbose_name='کاربر')
    phone = models.CharField(max_length=11, verbose_name='شماره تلفن')
    date_of_birth = models.DateField('تاریخ تولد')
    address = models.CharField('آدرس', max_length=200)
    join_date = models.DateField('تاریخ عضویت', auto_now_add=True)
    courses = models.ManyToManyField(Course, verbose_name='دوره ها')
    degree_choices = (
        ('دیپلم', 'دیپلم'),
        ('فوق دیپلم', 'فوق دیپلم'),
        ('لیسانس', 'لیسانس'),
        ('فوق لیسانس', 'فوق لیسانس'),
        ('دکتری', 'دکتری'),
    )
    degree = models.CharField('مدرک', max_length=10, choices=degree_choices)

    def get_full_name(self):
        return self.user.first_name + ' ' + self.user.last_name

    def jdate_of_birth(self):
        return digits.en_to_fa(JalaliDate(self.date_of_birth).strftime('%A %d %B %Y'))

    def jjoin_date(self):
        return digits.en_to_fa(JalaliDate(self.join_date).strftime('%A %d %B %Y'))

    def __str__(self):
        return self.usser.first_name + ' ' + self.usser.last_name



class Mark(models.Model):
    class Meta:
        verbose_name = 'نمره'
        verbose_name_plural = 'نمره'
    student = models.ForeignKey(Student, on_delete=models.PROTECT, verbose_name='دانشجو')
    course = models.ForeignKey(Course, on_delete=models.PROTECT, verbose_name='دوره')
    mark = models.IntegerField('نمره')

    def __str__(self):
        return self.student.name + ' ' + self.course.name



class Homework(models.Model):
    class Meta:
        verbose_name = 'آزمون'
        verbose_name_plural = 'آزمون'
    course = models.ForeignKey(Course, on_delete=models.PROTECT, verbose_name='دوره')
    title = models.CharField(max_length=50, verbose_name='عنوان')
    description = models.TextField(verbose_name='توضیحات')
    deadline = models.DateField(verbose_name='زمان تحویل')
    upload_time = models.DateField(verbose_name='زمان آپلود', auto_now_add=True)
    upload_file = models.FileField(verbose_name='فایل آپلود شده', upload_to='homework/')

    def __str__(self):
        return self.title

    def jdeadline(self):
        return digits.en_to_fa(JalaliDate(self.deadline).strftime('%A %d %B %Y'))

class Answer(models.Model):
    class Meta:
        verbose_name = 'پاسخ'
        verbose_name_plural = 'پاسخ'
    homework = models.ForeignKey(Homework, on_delete=models.PROTECT, verbose_name='آزمون')
    student = models.ForeignKey(Student, on_delete=models.PROTECT, verbose_name='دانشجو')
    answer = models.FileField(verbose_name='پاسخ دانشجو', upload_to='answer/')

    def __str__(self):
        return self.student.name + ' ' + self.homework.title