from django.urls import path
from . import views
app_name = 'main'
urlpatterns = [
    path('', views.index, name='index'),
    path('pricing/', views.pricing, name='pricing'),
    path('users/', views.users, name='users'),
    path('user_add/', views.user_add, name='user_add'),
    path('teachers/', views.teachers, name='teachers'),
    path('courses/', views.courses, name='courses'),
    path('course_add/', views.course_add, name='course_add'),
    path('course_edit/<int:course_id>/', views.course_edit, name='course_edit'),
    path('course_delete/<int:course_id>/', views.course_delete, name='course_delete'),
    path('not_found/', views.not_found, name='not_found'),
    path('teacher_edit/<int:teacher_id>/', views.teacher_edit, name='teacher_edit'),
    path('teacher_delete/<int:teacher_id>/', views.teacher_delete, name='teacher_delete'),
    path('teacher_add/', views.teacher_add, name='teacher_add'),
    path('students/', views.students, name='students'),
    path('student_add/', views.student_add, name='student_add'),
    path('student_edit/<int:student_id>/', views.student_edit, name='student_edit'),
    path('student_delete/<int:student_id>/', views.student_delete, name='student_delete'),
    
]
 