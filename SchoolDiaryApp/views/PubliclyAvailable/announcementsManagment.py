from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from SchoolDiaryApp.models_directory.structures import School, Announcements
from SchoolDiaryApp.models import Teacher, Director, Student
from SchoolDiaryApp.permissions import IsDirector, IsTeacher, IsStudent
from SchoolDiaryApp.serializers import AnnouncementsSerializer
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([IsDirector, IsTeacher, IsStudent])
def get_announcements(request):
    user = request.user
    if user.groups.filter(name='Director').exists():
        director = get_object_or_404(Director, user=user)
        school = director.school

    elif user.groups.filter(name='Teacher').exists():
        teacher = get_object_or_404(Teacher, user=user)
        school = School.objects.filter(classes__supervising_teacher=teacher).distinct().first()

    elif user.groups.filter(name='Student').exists():
        student = get_object_or_404(Student, user=user)
        school = student.class_id.school
    else:
        return Response({"error": "User does not belong to a school-related group."},
                        status=status.HTTP_403_FORBIDDEN)

    announcements = Announcements.objects.filter(school=school).order_by('-date')
    serializer = AnnouncementsSerializer(announcements, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsDirector, IsTeacher])
def post_announcements(request):
    user = request.user
    if user.groups.filter(name='Director').exists():
        director = get_object_or_404(Director, user=user)
        school = director.school

    elif user.groups.filter(name='Teacher').exists():
        teacher = get_object_or_404(Teacher, user=user)
        school = School.objects.filter(classes__supervising_teacher=teacher).distinct().first()

    else:
        return Response({"error": "User does not belong to a school-related group."},
                        status=status.HTTP_403_FORBIDDEN)

    data = request.data
    serializer = AnnouncementsSerializer(data=data)
    if serializer.is_valid():
        serializer.save(school=school, author=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)