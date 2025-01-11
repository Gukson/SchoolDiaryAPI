from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from SchoolDiaryApp.models_directory.structures import School, Announcements
from SchoolDiaryApp.models import Teacher, Director, Student, Admin, Parent
from SchoolDiaryApp.permissions import IsDirector, IsTeacher, IsStudent
from SchoolDiaryApp.serializers import AnnouncementsSerializer, TeacherSerializer, StudentSerializer, \
    DirectorSerializer, ParentSerializer, AdminSerializer
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def who_am_i(request):
    user = request.user
    user_data = {
        "Name": user.Name,
        "Surname": user.Surname,
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "user_type": user.user_type,
    }

    if user.user_type == "Teacher":
        teacher = get_object_or_404(Teacher, user=user)
        serializer = TeacherSerializer(teacher)
        user_data['details'] = serializer.data

    elif user.user_type == "Student":
        student = get_object_or_404(Student, user=user)
        serializer = StudentSerializer(student)
        user_data['details'] = serializer.data

    elif user.user_type == "Director":
        director = get_object_or_404(Director, user=user)
        serializer = DirectorSerializer(director)
        user_data['details'] = serializer.data

    elif user.user_type == "Parent":
        parent = get_object_or_404(Parent, user=user)
        serializer = ParentSerializer(parent)
        user_data['details'] = serializer.data

    elif user.user_type == "Administrator":
        admin = get_object_or_404(Admin, user=user)
        serializer = AdminSerializer(admin)
        user_data['details'] = serializer.data

    else:
        return Response(
            {"error": "User type not recognized or user does not belong to any specific group."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user_data["details"].pop("user", None)

    return Response(user_data, status=status.HTTP_200_OK)