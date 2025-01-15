from datetime import datetime

from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from SchoolDiaryApp.permissions import *
from rest_framework.response import Response
from rest_framework import status
from SchoolDiaryApp.models_directory.structures import Message, Class, Classes, School
from SchoolDiaryApp.models import CustomUser, Student, Director, Teacher, Admin
from SchoolDiaryApp.serializers import SubjectSerializer, ClassSerializer, ClassesSerializer, MessageSerializer, \
    StudentSerializer, TeacherSerializer, DirectorSerializer, AdminSerializer
from collections import defaultdict


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request):
    data = request.data

    content = data.get('content')
    topic = data.get('topic')
    address_id = data.get('address_id')

    if not content or not topic or not address_id:
        return Response(
            {"error": "Wszystkie pola (content, topic, address_id) są wymagane."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        address = CustomUser.objects.get(id=address_id)
    except CustomUser.DoesNotExist:
        return Response(
            {"error": "Użytkownik o podanym ID nie istnieje."},
            status=status.HTTP_404_NOT_FOUND
        )

    # Tworzenie wiadomości
    new_message = Message.objects.create(
        content=content,
        topic=topic,
        sender=request.user,
        address=address
    )

    return Response(
        {"message": "Wiadomość została pomyślnie wysłana."},
        status=status.HTTP_201_CREATED
    )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_received_messages(request):
    user = request.user
    received_messages = Message.objects.filter(address=user).order_by('-date')
    serializer = MessageSerializer(received_messages, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_sent_messages(request):
    user = request.user
    sent_messages = Message.objects.filter(sender=user).order_by('-date')
    serializer = MessageSerializer(sent_messages, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_message_status(request, message_id):
    user = request.user  # Aktualny użytkownik

    try:
        message = Message.objects.get(id=message_id, address=user)
    except Message.DoesNotExist:
        return Response(
            {"error": "Wiadomość nie istnieje lub nie masz do niej dostępu."},
            status=status.HTTP_404_NOT_FOUND
        )

    read_status = request.data.get('read')
    if read_status is not None:
        message.read = read_status

    message.save()

    return Response(
        {"message": "Status wiadomości został zaktualizowany."},
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
def get_students(request):
    user = request.user
    students_by_school = defaultdict(list)
    print(user.groups.all())

    if user.groups.filter(name='Director').exists():
        director = get_object_or_404(Director, user=user)
        school = director.school  # Szkoła przypisana do dyrektora
        students = Student.objects.filter(class_id__school=school)
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Jeśli użytkownik jest nauczycielem
    elif user.groups.filter(name='Teacher').exists():
        teacher = get_object_or_404(Teacher, user=user)



        classes_taught = Classes.objects.filter(teacher=teacher)

        print("siema")
        #TODO zmienić to
        schools = School.objects.filter(classes_school=classes_taught).distinct()

        print("siema1")
        students = Student.objects.filter(class_id__school__in=schools)
        for student in students:
            school_name = student.class_id.school.name
            students_by_school[school_name].append(student)


        grouped_data = []
        for school_name, students in students_by_school.items():
            serializer = StudentSerializer(students, many=True)
            grouped_data.append({
                "school": school_name,
                "students": serializer.data
            })

        return Response(grouped_data, status=status.HTTP_200_OK)

    elif user.groups.filter(name='Administrator').exists():
        students = Student.objects.get()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response({"error": "Brak uprawnień do wykonania tego zapytania."},
                    status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
def get_teachers(request):
    user = request.user
    if user.groups.filter(name='Director').exists():
        director = get_object_or_404(Director, user=user)
        school = director.school

        teachers = Teacher.objects.filter(class_teacher__class_id__school=school).distinct()

        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if user.groups.filter(name='Administrator').exists():
        teachers = Teacher.objects.get()
        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if user.groups.filter(name='Student').exists():
        student = get_object_or_404(Student, user=user)
        school = student.class_id.school
        teachers = Teacher.objects.filter(class_teacher__class_id__school=school).distinct()
        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if user.groups.filter(name='Teacher').exists():
        teacher = get_object_or_404(Teacher, user=user)

        schools = School.objects.filter(classes__supervising_teacher=teacher).distinct()

        teachers = Teacher.objects.filter(class_teacher__class_id__school__in=schools).distinct()
        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_directors(request):
    user = request.user
    if user.groups.filter(name='Director').exists():
        # Dyrektor widzi wszystkich dyrektorów swojej szkoły
        director = get_object_or_404(Director, user=user)
        school = director.school
        directors = Director.objects.filter(school=school).distinct()
        serializer = DirectorSerializer(directors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if user.groups.filter(name='Administrator').exists():
        # Administrator widzi wszystkich dyrektorów
        directors = Director.objects.all()
        serializer = DirectorSerializer(directors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if user.groups.filter(name='Student').exists():
        # Student widzi dyrektorów swojej szkoły
        student = get_object_or_404(Student, user=user)
        school = student.class_id.school
        directors = Director.objects.filter(school=school).distinct()
        serializer = DirectorSerializer(directors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if user.groups.filter(name='Teacher').exists():
        # Nauczyciel widzi dyrektorów szkół, w których pracuje
        teacher = get_object_or_404(Teacher, user=user)
        schools = School.objects.filter(classes__supervising_teacher=teacher).distinct()
        directors = Director.objects.filter(school__in=schools).distinct()
        serializer = DirectorSerializer(directors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Jeśli użytkownik nie należy do żadnej uprawnionej grupy
    return Response({"error": "You do not have permission to view this data."},
                    status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
def get_admins(request):
    admins = Admin.objects.all()
    serializer = AdminSerializer(admins, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
