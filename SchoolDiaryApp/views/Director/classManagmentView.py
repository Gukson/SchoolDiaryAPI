from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from SchoolDiaryApp.permissions import IsDirector
from rest_framework.response import Response
from rest_framework import status

from SchoolDiaryApp.models_directory.structures import Class, School
from SchoolDiaryApp.models import Student, Teacher, Director

from SchoolDiaryApp.serializers import ClassSerializer, StudentSerializer


@api_view(['GET', 'POST'])
@permission_classes([IsDirector])
def classes_view(request):
    director = get_object_or_404(Director, user=request.user)
    try:
        school = director.school
    except School.DoesNotExist:
        return Response({'error': 'School not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        classes = Class.objects.filter(school=school)
        serializer = ClassSerializer(classes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        data = request.data
        data['school'] = school.id

        serializer = ClassSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsDirector])
def class_view(request, name):
    director = get_object_or_404(Director, user=request.user)
    if request.method == 'GET':
        school = director.school
        try:
            class_ = Class.objects.get(name=name, school=school)
        except Class.DoesNotExist:
            return Response({'error': 'Class not found'}, status=status.HTTP_404_NOT_FOUND)

        students = Student.objects.filter(class_id=class_)
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'PATCH':
        school = director.school
        class_ = get_object_or_404(Class, name=name, school=school)
        print("siema")
        supervising_teacher_id = request.data.get('supervising_teacher')
        if supervising_teacher_id:

            teacher = get_object_or_404(Teacher, id=supervising_teacher_id)
            class_.supervising_teacher = teacher

        new_name = request.data.get('name')
        if new_name:
            class_.name = new_name

        class_.save()

        serializer = ClassSerializer(class_)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'DELETE':
        school = director.school
        class_ = get_object_or_404(Class, name=name, school=school)
        class_.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

