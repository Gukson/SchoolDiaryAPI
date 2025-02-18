from rest_framework import permissions
from django.contrib.auth.models import Group


class IsAdministrator(permissions.BasePermission):
    message = "Nie masz uprawnień, aby uzyskać dostęp do tej zawartości."
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Administrator').exists()

    def has_object_permission(self, request, view, obj):
        return request.user.groups.filter(name='Administrator').exists()


class IsDirector(permissions.BasePermission):
    message = "Nie masz uprawnień, aby uzyskać dostęp do tej zawartości."
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Director').exists()

    def has_object_permission(self, request, view, obj):
        return request.user.groups.filter(name='Director').exists()


class IsParent(permissions.BasePermission):
    message = "Nie masz uprawnień, aby uzyskać dostęp do tej zawartości."
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Parent').exists()

    def has_object_permission(self, request, view, obj):
        return request.user.groups.filter(name='Parent').exists()


class IsStudent(permissions.BasePermission):
    message = "Nie masz uprawnień, aby uzyskać dostęp do tej zawartości."
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Student').exists()

    def has_object_permission(self, request, view, obj):
        return request.user.groups.filter(name='Student').exists()


class IsTeacher(permissions.BasePermission):
    message = "Nie masz uprawnień, aby uzyskać dostęp do tej zawartości."
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Teacher').exists()

    def has_object_permission(self, request, view, obj):
        return request.user.groups.filter(name='Teacher').exists()