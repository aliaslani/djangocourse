from django.urls import path
from . import views
app_name = 'main'
urlpatterns = [
    path('', views.index, name='index'),
    path('pricing/', views.pricing, name='pricing'),
    path('users/', views.users, name='users'),
    path('teachers/', views.teachers, name='teachers'),
    path('courses/', views.courses, name='courses'),
    path('not_found/', views.not_found, name='not_found'),
    
]
 