from django.contrib import admin
from account.models import Teacher, Course, Student, Mark, Homework, Answer

# Register your models here.

admin.site.register(Teacher)
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Mark)
admin.site.register(Homework)
admin.site.register(Answer)
