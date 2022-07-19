from django.db import models

# Create your models here.

class Teacher(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone = models.IntegerField()
    age = models.IntegerField()
    experieces = models.IntegerField()


    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=50)
    length = models.IntegerField()
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

class Student(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone = models.IntegerField()
    age = models.IntegerField()
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING)
    score = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


