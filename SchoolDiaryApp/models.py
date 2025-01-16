from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, BaseUserManager
from SchoolDiaryApp.models_directory.structures import *
from datetime import date



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
        extra_fields.setdefault('birth_date', date(2000, 1, 1))

        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractUser):
    objects = CustomUserManager()
    USER_TYPE_CHOICES = (
        ('Student', 'Student'),
        ('Teacher', 'Nauczyciel'),
        ('Director', 'Dyrektor'),
        ('Parent', 'Rodzic'),
        ('Administrator', 'Administrator'),
    )
    user_type = models.CharField(max_length=15, choices=USER_TYPE_CHOICES, default='student')
    pesel = models.CharField(max_length=11)
    login = models.CharField(max_length=255, unique=True)
    Name = models.CharField(max_length=255)
    Surname = models.CharField(max_length=255)
    birth_date = models.DateField()

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        group_name = self.user_type
        group, created = Group.objects.get_or_create(name=group_name)
        self.groups.add(group)

    groups = models.ManyToManyField(
        Group,
        blank=True,
        related_name='customuser_groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name='customuser_permissions'
    )

class Parent(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.PROTECT)

class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.PROTECT)
    parent = models.ForeignKey(
        Parent,
        on_delete=models.SET_NULL,
        related_name='parent_child',
        blank=True,
        null=True
    )
    class_id = models.ForeignKey(
        Class,
        on_delete=models.PROTECT,
        related_name='students_class',
        null=True,
        blank=True
    )
    school = models.ForeignKey(
        School,
        on_delete=models.PROTECT,
        related_name='students_school',
        null=True,
        blank=True
    )

class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.PROTECT)
    school = models.ForeignKey(
        School,
        on_delete=models.PROTECT,
        related_name='teachers_school',
        null=True,
        blank=True
    )

class Director(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.PROTECT)
    school = models.ForeignKey(
        School,
        on_delete=models.PROTECT,
        related_name='directors_school',
        null=True,
        blank=True
    )

class Admin(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.PROTECT)