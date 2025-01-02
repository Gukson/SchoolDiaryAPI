from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

from django.contrib.auth.models import Group
from django.db import models
from django.contrib.auth.models import AbstractUser

from django.contrib.auth.models import AbstractUser, Group, Permission

from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        if not username:
            raise ValueError('Username is required')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        # Ustaw domyślne wartości dla brakujących pól, jeśli wymagane
        extra_fields.setdefault('Name', 'Super')
        extra_fields.setdefault('Surname', 'Admin')
        extra_fields.setdefault('pesel', '00000000000')
        extra_fields.setdefault('birth_date', '2000-01-01')

        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('Student', 'Uczeń'),
        ('Teacher', 'Nauczyciel'),
        ('Director', 'Dyrektor'),
        ('Parent', 'Rodzic'),
        ('Administrator', 'Administrator'),
    )
    user_type = models.CharField(max_length=15, choices=USER_TYPE_CHOICES, default='student')
    pesel = models.CharField(max_length=11, unique=True)
    login = models.CharField(max_length=255, unique=True)
    Name = models.CharField(max_length=255)
    Surname = models.CharField(max_length=255)
    birth_date = models.DateField()

    # objects = CustomUserManager()  # Użyj niestandardowego menedżera

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
    id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=255)
    school = models.ForeignKey(School, on_delete=models.PROTECT, related_name='classes_school')
    supervising_teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT, related_name='supervising_teacher')


class Subject(models.Model):
    subject_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=20)


class Classes(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    date = models.DateField()
    lesson_num = models.IntegerField()
    class_id = models.ForeignKey(Class, on_delete=models.PROTECT, related_name='classe_id')
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT, related_name='class_subject')
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT, related_name='class_teacher')


class Grate(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.IntegerField()
    weight = models.IntegerField()
    category = models.CharField(max_length=20, unique=True)
    description = models.TextField(max_length=1000)
    class_id = models.ForeignKey(Classes, on_delete=models.PROTECT, related_name='grated_class')
    student = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='grated_student')


class Announcements(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    topic = models.CharField(max_length=255)
    content = models.TextField(max_length=1000)
    date = models.DateField()
    school = models.ForeignKey(School, on_delete=models.PROTECT, related_name='announcements_school')
    author = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='author_of_announcement')


class Frequency(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    type = models.CharField(max_length=2)
    student = models.ForeignKey(Student, on_delete=models.PROTECT, related_name='students_frequency')
    class_id = models.ForeignKey(Classes, on_delete=models.PROTECT, related_name='frequencies_class')


class Event(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    date = models.DateField()
    category = models.CharField(max_length=20)
    subject = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    class_id = models.ForeignKey(Class, on_delete=models.PROTECT, related_name='class_event')
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT, related_name='author_of_event')
