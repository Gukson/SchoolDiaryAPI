from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

from django.contrib.auth.models import Group
from django.db import models
from django.contrib.auth.models import AbstractUser


from django.contrib.auth.models import AbstractUser, Group, Permission

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('Student', 'Uczeń'),
        ('Teacher', 'Nauczyciel'),
        ('Director', 'Dyrektor'),
        ('Parent', 'Rodzic'),
        ('Administrator', 'Administrator'),
    )
    user_type = models.CharField(max_length=15, choices=USER_TYPE_CHOICES, default='student')
    id = models.IntegerField(primary_key=True, unique=True)
    pesel = models.CharField(max_length=11, unique=True)
    login = models.CharField(max_length=255, unique=True)
    Name = models.CharField(max_length=255)
    Surname = models.CharField(max_length=255)
    birth_date = models.DateField()

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        # Zapisanie użytkownika w bazie
        super().save(*args, **kwargs)

        # Przypisanie użytkownika do odpowiedniej grupy na podstawie user_type
        group_name = self.user_type  # nazwa grupy, np. 'teacher'

        # Sprawdzenie, czy grupa istnieje, i dodanie użytkownika do grupy
        group, created = Group.objects.get_or_create(name=group_name)

        # Dodanie użytkownika do grupy
        self.groups.add(group)

    # Dodajemy unikalne related_name do grup i uprawnień
    groups = models.ManyToManyField(
        Group,
        blank=True,
        related_name='customuser_groups'  # Unikalny related_name dla grup
    )
    user_permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name='customuser_permissions'  # Unikalny related_name dla uprawnień
    )



class School(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)
    id = models.IntegerField(primary_key=True, unique=True)


class Parent(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.PROTECT)


class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.PROTECT)
    parent = models.ForeignKey(Parent, on_delete=models.SET_NULL, related_name='parent_child', blank=True, null=True)


class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.PROTECT)


class Director(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.PROTECT)
    school = models.ForeignKey(School, on_delete=models.PROTECT, related_name='directors_school')


class Admin(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.PROTECT)


class Message(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    date = models.DateField()
    topic = models.CharField(max_length=100)
    content = models.TextField(max_length=1000)
    address = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        related_name='received_messages'  # Custom related_name for address
    )
    sender = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        related_name='sent_messages'  # Custom related_name for sender
    )



class Class(models.Model):
    class_id = models.IntegerField(primary_key=True, unique=True)
    Name = models.CharField(max_length=255)
    school = models.ForeignKey(School, on_delete=models.PROTECT, related_name='classes_school')
    supervising_teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT, related_name='supervising_teacher')


class Subject(models.Model):
    subject_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=20)


class Classes(models.Model):
    classes_id = models.IntegerField(primary_key=True, unique=True)
    date = models.DateField()
    lesson_num = models.IntegerField()
    class_id = models.ForeignKey(Class, on_delete=models.PROTECT, related_name='classe_id')
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT, related_name='class_subject')
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT, related_name='class_teacher')


class Grate(models.Model):
    grate_id = models.IntegerField(primary_key=True)
    value = models.IntegerField()
    weight = models.IntegerField()
    category = models.CharField(max_length=20, unique=True)
    description = models.TextField(max_length=1000)
    class_id = models.ForeignKey(Classes, on_delete=models.PROTECT, related_name='grated_class')
    student = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='grated_student')


class Announcements(models.Model):
    announcement_id = models.IntegerField(primary_key=True, unique=True)
    topic = models.CharField(max_length=255)
    content = models.TextField(max_length=1000)
    date = models.DateField()
    school = models.ForeignKey(School, on_delete=models.PROTECT, related_name='announcements_school')
    author = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='author_of_announcement')


class Frequency(models.Model):
    frequency_id = models.IntegerField(primary_key=True, unique=True)
    type = models.CharField(max_length=2)
    student = models.ForeignKey(Student, on_delete=models.PROTECT, related_name='students_frequency')
    class_id = models.ForeignKey(Classes, on_delete=models.PROTECT, related_name='frequencies_class')


class Event(models.Model):
    event_id = models.IntegerField(primary_key=True, unique=True)
    date = models.DateField()
    category = models.CharField(max_length=20)
    subject = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    class_id = models.ForeignKey(Class, on_delete=models.PROTECT, related_name='class_event')
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT, related_name='author_of_event')
