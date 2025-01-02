from django.contrib import admin
from django.contrib import admin
from .models import CustomUser, Parent, Student, Teacher, Director, Admin, School


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'user_type', 'Name', 'Surname', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'Name', 'Surname', 'pesel')
    list_filter = ('user_type', 'is_active', 'is_staff')


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    search_fields = ('user__username', 'user__Name', 'user__Surname')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'parent')
    search_fields = ('user__username', 'user__Name', 'user__Surname', 'parent__user__Name', 'parent__user__Surname')
    list_filter = ('parent',)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    search_fields = ('user__username', 'user__Name', 'user__Surname')


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'school')
    search_fields = ('user__username', 'user__Name', 'user__Surname', 'school__name')
    list_filter = ('school',)


@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    search_fields = ('user__username', 'user__Name', 'user__Surname')