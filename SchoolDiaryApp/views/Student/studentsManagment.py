from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from SchoolDiaryApp.permissions import IsDirector, IsTeacher
from SchoolDiaryApp.models import CustomUser, Student,Parent, Teacher, Director, Admin, CustomUser
from SchoolDiaryApp.models_directory.structures import School, Class
from SchoolDiaryApp.serializers import CustomUserSerializer, StudentSerializer, ParentSerializer, TeacherSerializer, DirectorSerializer, AdminSerializer, CustomUserSerializer


@api_view(['GET', 'POST', 'DELETE', 'PATCH'])
@permission_classes([IsDirector, IsTeacher])
def manage_students(request):
    try:
        # Próbuj pobrać dyrektora
        director = Director.objects.get(user=request.user)
        school = director.school
    except Director.DoesNotExist:
        try:
            # Jeśli nie jest dyrektorem, próbuj pobrać nauczyciela
            teacher = Teacher.objects.get(user=request.user)
            # Pobierz szkoły, w których nauczyciel uczy
            school = teacher.school
        except Teacher.DoesNotExist:
            return Response({"error": "User does not have access to manage students."},
                            status=403)

    if request.method == 'GET':
        students = Student.objects.filter(school=school).order_by('user__last_name', 'user__first_name')
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        pesel = request.data.get('pesel')

        existing_student = Student.objects.filter(
            user__pesel=pesel,
            class_id__school=school
        ).first()

        if existing_student:
            return Response(
                {'error': 'Student with this PESEL already exists in this school'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user_serializer = CustomUserSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save(user_type='Student')  # Typ użytkownika ustawiony na 'Student'
            student = Student.objects.create(user=user, school=school)
            student_serializer = StudentSerializer(student)
            return Response(student_serializer.data, status=status.HTTP_201_CREATED)

        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        class_id = request.data.get('class_id')
        student = get_object_or_404(Student, id=request.data.get('student_id'), school=director.school)
        student.class_id = get_object_or_404(Class, id=class_id, school=director.school)
        student.save()
        return Response(status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        student_id = request.data.get('student_id')
        student = get_object_or_404(Student, id=student_id, school=school)
        student.school = None
        return Response(status=status.HTTP_204_NO_CONTENT)



# Zarządzanie rodzicami
@api_view(['GET', 'POST'])
def manage_parents(request):
    if request.method == 'GET':
        parents = Parent.objects.all()
        serializer = ParentSerializer(parents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        user_serializer = CustomUserSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save(user_type='Parent')  # Domyślnie typ użytkownika ustawiony na "Parent"
            parent = Parent.objects.create(user=user)
            parent_serializer = ParentSerializer(parent)
            return Response(parent_serializer.data, status=status.HTTP_201_CREATED)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



