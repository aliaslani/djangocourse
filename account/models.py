from django.db import models

# Create your models here.

class Teacher(models.Model):
    class Meta:
        verbose_name = 'استاد'
        verbose_name_plural = 'استاد'
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone = models.IntegerField()
    age = models.IntegerField()
    experieces = models.IntegerField()


    def __str__(self):
        return self.name

class Course(models.Model):
    class Meta:
        verbose_name = 'دوره'
        verbose_name_plural = 'دوره '
    name = models.CharField(max_length=50)
    length = models.IntegerField()
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

class Student(models.Model):
    class Meta:
        verbose_name = 'دانشجو'
        verbose_name_plural = 'دانشجو'
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone = models.IntegerField()
    age = models.IntegerField()
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING)
    score = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


