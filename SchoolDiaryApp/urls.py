from django.urls import path
from SchoolDiaryApp.views.Student.studentsManagment import *
from .views.schoolManagementView import *
from SchoolDiaryApp.views.Director.classesManagment import *
from SchoolDiaryApp.views.Teacher.teacherManagment import *
from SchoolDiaryApp.views.Director.classManagmentView import *
from SchoolDiaryApp.views.PubliclyAvailable.messagesManagmentView import *
from SchoolDiaryApp.views.Teacher.frequencyManagment import *
from SchoolDiaryApp.views.Student.gratesManagment import *
from SchoolDiaryApp.views.PubliclyAvailable.announcementsManagment import *
from SchoolDiaryApp.views.PubliclyAvailable.meManagment import *
from SchoolDiaryApp.views.Student.studentClassesManagment import *

urlpatterns = [

    #zarządzanie użytkownikami
    path('me/', who_am_i, name='who_am_i'),
    path('students/', manage_students, name='manage_students'),
    path('teachers/', manage_teachers, name='manage_teachers'),

    #odebrane wiadomości
    path('get_received_messages/', get_received_messages, name='get_received_messages'),

    # Wysłane wiadomości
    path('get_sent_messages/', get_sent_messages, name='get_sent_messages'),

    # Aktualizacja statusu wiadomości (np. odczytane/nieodczytane)
    path('update_message_status/<int:message_id>/', update_message_status, name='update_message_status'),

    # Wysyłanie nowej wiadomości
    path('send_message/', send_message, name='send_message'),

    #--------------------

    #Zarządzanie klasami
    path('class/', classes_view, name='classes_view'),

    #Zarządzanie przedmiotami
    path('subjects/', subject_view, name='subject_view'),

    #Zarządzanie zajęciami
    path('classes/', create_recurring_classes, name='create_recurring_classes'),

    # zarządzanie frekwencją
    path('classes/frequency/', class_frequency, name='class_frequency'),
    path('students/frequency/', student_frequency, name='student_frequency'),

    #--------------------

    #odbieranie ogłoszeń
    path('get_announcements/',get_announcements,name='get_announcements'),

    #wysyłanei ogłoszeń
    path('post_announcements/',post_announcements,name='get_announcements'),



    #------------------


    #Uczeń
    #przegldaj oceny
    path('students/grates/', get_student_grades, name='get_student_grades'),
    path('students/classes', get_student_classes, name='get_student_classes'),
    #================================================
    path('parents/', manage_parents, name='manage_parents'),
    path('schools/',school_view,name='school_view'),


]
