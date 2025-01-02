from django.urls import path
from .views.StudentListCreateAPIView import *


urlpatterns = [
    path('students/', manage_students, name='manage_students'),
    path('students/<int:pk>/', manage_single_student, name='manage_single_student'),
    path('parents/', manage_parents, name='manage_parents'),
    path('parents/<int:pk>/', manage_single_parent, name='manage_single_parent'),
    path('teachers/', manage_teachers, name='manage_teachers'),
    path('teachers/<int:pk>/', manage_single_teacher, name='manage_single_teacher'),
    path('directors/', manage_directors, name='manage_directors'),
    path('directors/<int:pk>/', manage_single_director, name='manage_single_director'),
    path('admins/', manage_admins, name='manage_admins'),
    path('admins/<int:pk>/', manage_single_admin, name='manage_single_admin'),

]
