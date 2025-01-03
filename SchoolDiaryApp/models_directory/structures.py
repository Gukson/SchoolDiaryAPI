# from django.db import models_directory
#
# from django.contrib.auth.models_directory import AbstractUser
# from django.contrib.auth.models_directory import Group
# from django.contrib.auth.models_directory import AbstractUser
# from django.contrib.auth.models_directory import AbstractUser, Group, Permission
# from django.contrib.auth.models_directory import BaseUserManager
#
# class Message(models_directory.Model):
#     id = models_directory.IntegerField(primary_key=True, unique=True)
#     date = models_directory.DateField()
#     topic = models_directory.CharField(max_length=100)
#     content = models_directory.TextField(max_length=1000)
#     address = models_directory.ForeignKey(
#         CustomUser,
#         on_delete=models_directory.PROTECT,
#         related_name='received_messages'  # Custom related_name for address
#     )
#     sender = models_directory.ForeignKey(
#         CustomUser,
#         on_delete=models_directory.PROTECT,
#         related_name='sent_messages'  # Custom related_name for sender
#     )
#
#
# class Class(models_directory.Model):
#     id = models_directory.IntegerField(primary_key=True, unique=True)
#     name = models_directory.CharField(max_length=255)
#     school = models_directory.ForeignKey(School, on_delete=models_directory.PROTECT, related_name='classes_school')
#     supervising_teacher = models_directory.ForeignKey(Teacher, on_delete=models_directory.PROTECT, related_name='supervising_teacher')
#
#
# class Subject(models_directory.Model):
#     subject_id = models_directory.CharField(max_length=10, unique=True)
#     name = models_directory.CharField(max_length=20)
#
#
# class Classes(models_directory.Model):
#     id = models_directory.IntegerField(primary_key=True, unique=True)
#     date = models_directory.DateField()
#     lesson_num = models_directory.IntegerField()
#     class_id = models_directory.ForeignKey(Class, on_delete=models_directory.PROTECT, related_name='classe_id')
#     subject = models_directory.ForeignKey(Subject, on_delete=models_directory.PROTECT, related_name='class_subject')
#     teacher = models_directory.ForeignKey(Teacher, on_delete=models_directory.PROTECT, related_name='class_teacher')
#
#
# class Grate(models_directory.Model):
#     id = models_directory.IntegerField(primary_key=True)
#     value = models_directory.IntegerField()
#     weight = models_directory.IntegerField()
#     category = models_directory.CharField(max_length=20, unique=True)
#     description = models_directory.TextField(max_length=1000)
#     class_id = models_directory.ForeignKey(Classes, on_delete=models_directory.PROTECT, related_name='grated_class')
#     student = models_directory.ForeignKey(CustomUser, on_delete=models_directory.PROTECT, related_name='grated_student')
#
#
# class Announcements(models_directory.Model):
#     id = models_directory.IntegerField(primary_key=True, unique=True)
#     topic = models_directory.CharField(max_length=255)
#     content = models_directory.TextField(max_length=1000)
#     date = models_directory.DateField()
#     school = models_directory.ForeignKey(School, on_delete=models_directory.PROTECT, related_name='announcements_school')
#     author = models_directory.ForeignKey(CustomUser, on_delete=models_directory.PROTECT, related_name='author_of_announcement')
#
#
# class Frequency(models_directory.Model):
#     id = models_directory.IntegerField(primary_key=True, unique=True)
#     type = models_directory.CharField(max_length=2)
#     student = models_directory.ForeignKey(Student, on_delete=models_directory.PROTECT, related_name='students_frequency')
#     class_id = models_directory.ForeignKey(Classes, on_delete=models_directory.PROTECT, related_name='frequencies_class')
#
#
# class Event(models_directory.Model):
#     id = models_directory.IntegerField(primary_key=True, unique=True)
#     date = models_directory.DateField()
#     category = models_directory.CharField(max_length=20)
#     subject = models_directory.CharField(max_length=100)
#     description = models_directory.TextField(max_length=1000)
#     class_id = models_directory.ForeignKey(Class, on_delete=models_directory.PROTECT, related_name='class_event')
#     teacher = models_directory.ForeignKey(Teacher, on_delete=models_directory.PROTECT, related_name='author_of_event')
