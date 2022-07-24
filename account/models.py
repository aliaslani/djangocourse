from django.db import models

# Create your models here.


class Teacher(models.Model):
    class Meta:
        verbose_name = 'استاد'
        verbose_name_plural = 'استاد'
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, verbose_name='کاربر')
    name = models.CharField(max_length=50, verbose_name='نام')
    email = models.EmailField(max_length=50, verbose_name='ایمیل')
    phone = models.IntegerField('تلفن')
    age = models.IntegerField('سن')
    experieces = models.IntegerField('سابقه کاری')


    def __str__(self):
        return self.name

class Course(models.Model):
    class Meta:
        verbose_name = 'دوره'
        verbose_name_plural = 'دوره '
    name = models.CharField(max_length=50, verbose_name='نام دوره')
    length = models.IntegerField(verbose_name='طول دوره')
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT, verbose_name='استاد')
    status_choices = (
        ('1', 'در حال برگزاری'),
        ('2', 'برگزار شده'),
        ('3', 'پایان داده شده'),
    )
    status = models.CharField(max_length=1, choices=status_choices, verbose_name='وضعیت')

    def __str__(self):
        return self.name

class Student(models.Model):
    class Meta:
        verbose_name = 'دانشجو'
        verbose_name_plural = 'دانشجو'
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='student', verbose_name='کاربر')
    name = models.CharField(max_length=50, verbose_name='نام')
    email = models.EmailField(max_length=50, verbose_name='ایمیل')
    phone = models.IntegerField(verbose_name='شماره تلفن')
    age = models.IntegerField(verbose_name='سن')
    courses = models.ManyToManyField(Course, verbose_name='دوره ها')

    def __str__(self):
        return self.name

    def __str__(self):
        return self.name


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

class Answer(models.Model):
    class Meta:
        verbose_name = 'پاسخ'
        verbose_name_plural = 'پاسخ'
    homework = models.ForeignKey(Homework, on_delete=models.PROTECT, verbose_name='آزمون')
    student = models.ForeignKey(Student, on_delete=models.PROTECT, verbose_name='دانشجو')
    answer = models.FileField(verbose_name='پاسخ دانشجو', upload_to='answer/')

    def __str__(self):
        return self.student.name + ' ' + self.homework.title