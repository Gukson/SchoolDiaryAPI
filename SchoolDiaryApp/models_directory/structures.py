from django.db import models
from django.conf import settings

class School(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)

class Class(models.Model):
    name = models.CharField(max_length=255)
    school = models.ForeignKey(
        'SchoolDiaryApp.School',
        on_delete=models.PROTECT,
        related_name='classes_school'
    )
    supervising_teacher = models.ForeignKey(
        'SchoolDiaryApp.Teacher',
        on_delete=models.PROTECT,
        related_name='supervising_teacher',
        null=True,
        blank=True
    )

class Subject(models.Model):
    name = models.CharField(max_length=20)
    school = models.ForeignKey(
        'SchoolDiaryApp.School',
        on_delete=models.PROTECT,
        related_name='subjects_school',
        null=True,
        blank=True
    )

class Classes(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    date = models.DateField()
    time = models.TimeField()  # Dodane pole do przechowywania godziny rozpoczęcia
    lesson_num = models.IntegerField()
    class_id = models.ForeignKey(
        Class,
        on_delete=models.PROTECT,
        related_name='classe_id'
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.PROTECT,
        related_name='class_subject'
    )
    teacher = models.ForeignKey(
        'SchoolDiaryApp.Teacher',
        on_delete=models.PROTECT,
        related_name='class_teacher'
    )

class Grate(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.IntegerField()
    weight = models.IntegerField()
    category = models.CharField(max_length=20, unique=True)
    description = models.TextField(max_length=1000)
    class_id = models.ForeignKey(
        Classes,
        on_delete=models.PROTECT,
        related_name='grated_class'
    )
    student = models.ForeignKey(
        'SchoolDiaryApp.Student',
        on_delete=models.PROTECT,
        related_name='grated_student'
    )

class Announcements(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    topic = models.CharField(max_length=255)
    content = models.TextField(max_length=1000)
    date = models.DateField()
    school = models.ForeignKey(
        School,
        on_delete=models.PROTECT,
        related_name='announcements_school'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='author_of_announcement'
    )

class Frequency(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    type = models.CharField(max_length=2)
    student = models.ForeignKey(
        'SchoolDiaryApp.Student',
        on_delete=models.PROTECT,
        related_name='students_frequency'
    )
    class_id = models.ForeignKey(
        Classes,
        on_delete=models.PROTECT,
        related_name='frequencies_class'
    )

class Event(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    date = models.DateField()
    category = models.CharField(max_length=20)
    subject = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    class_id = models.ForeignKey(
        Class,
        on_delete=models.PROTECT,
        related_name='class_event'
    )
    teacher = models.ForeignKey(
        'SchoolDiaryApp.Teacher',
        on_delete=models.PROTECT,
        related_name='author_of_event'
    )

class Message(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    date = models.DateField()
    topic = models.CharField(max_length=100)
    content = models.TextField(max_length=1000)
    address = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='received_messages'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='sent_messages'
    )