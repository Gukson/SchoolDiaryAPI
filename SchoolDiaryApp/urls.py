from django.urls import path
from SchoolDiaryApp.views.Director.studentsManagment import *
from .views.schoolManagementView import *
from SchoolDiaryApp.views.Director.classManagmentView import *
from SchoolDiaryApp.views.Director.teacherManagment import *

urlpatterns = [
    #dyrektor - zarządzanie klasami
    path('schools/<int:school_id>/classes/', classes_view, name='classes_view'),
    path('schools/<int:school_id>/classes/<str:name>/', class_view, name='class_management'),

    #dyrektor - zarządzanie uczniami
    path('students/<int:school_id>/', manage_students, name='manage_students'),
    path('students/<int:pk>/', manage_single_student, name='manage_single_student'),
    path('students/class/', manage_student_class, name='manage_student_class'),

    #dyrektor - zarządzanie nauczycielami
    path('teachers/', manage_teachers, name='manage_teachers'),
    path('teachers/<int:pk>/', manage_single_teacher, name='manage_single_teacher'),


    #dyrektor - zarządzanie zajęciami



    path('parents/', manage_parents, name='manage_parents'),
    path('parents/<int:pk>/', manage_single_parent, name='manage_single_parent'),

    path('directors/', manage_directors, name='manage_directors'),
    path('directors/<int:pk>/', manage_single_director, name='manage_single_director'),
    path('admins/', manage_admins, name='manage_admins'),
    path('admins/<int:pk>/', manage_single_admin, name='manage_single_admin'),
    path('schools/',school_view,name='school_view'),


]
