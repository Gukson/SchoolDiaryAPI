from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import CustomUser, Student,Parent, Teacher, Director, Admin, CustomUser
from ..serializers import CustomUserSerializer, StudentSerializer, ParentSerializer, TeacherSerializer, DirectorSerializer, AdminSerializer, CustomUserSerializer

@api_view(['GET', 'POST'])
def manage_students(request):
    if request.method == 'GET':
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        user_serializer = CustomUserSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save(user_type='Student')  # Domyślnie typ użytkownika ustawiony na "Student"
            student = Student.objects.create(user=user)
            student_serializer = StudentSerializer(student)
            return Response(student_serializer.data, status=status.HTTP_201_CREATED)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def manage_single_student(request, pk):
    student = Student.objects.filter(id=pk)
    if not student.exists():
        return Response({"error": "Student does not exist"}, status=status.HTTP_400_BAD_REQUEST)
    serialized_order = StudentSerializer(student, many=True)
    return Response(serialized_order.data, status=status.HTTP_200_OK)




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


@api_view(['GET'])
def manage_single_parent(request, pk):
    parent = Parent.objects.filter(id=pk)
    if not parent.exists():
        return Response({"error": "Parent does not exist"}, status=status.HTTP_400_BAD_REQUEST)
    serializer = ParentSerializer(parent, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Zarządzanie nauczycielami
@api_view(['GET', 'POST'])
def manage_teachers(request):
    if request.method == 'GET':
        teachers = Teacher.objects.all()
        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        user_serializer = CustomUserSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save(user_type='Teacher')  # Domyślnie typ użytkownika ustawiony na "Teacher"
            teacher = Teacher.objects.create(user=user)
            teacher_serializer = TeacherSerializer(teacher)
            return Response(teacher_serializer.data, status=status.HTTP_201_CREATED)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def manage_single_teacher(request, pk):
    teacher = Teacher.objects.filter(id=pk)
    if not teacher.exists():
        return Response({"error": "Teacher does not exist"}, status=status.HTTP_400_BAD_REQUEST)
    serializer = TeacherSerializer(teacher, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Zarządzanie dyrektorami
@api_view(['GET', 'POST'])
def manage_directors(request):
    if request.method == 'GET':
        directors = Director.objects.all()
        serializer = DirectorSerializer(directors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        user_serializer = CustomUserSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save(user_type='Director')  # Domyślnie typ użytkownika ustawiony na "Director"
            school_id = request.data.get('school')  # Pobierz ID szkoły z requestu
            if not school_id:
                return Response({"error": "School is required for a Director"}, status=status.HTTP_400_BAD_REQUEST)
            director = Director.objects.create(user=user, school_id=school_id)
            director_serializer = DirectorSerializer(director)
            return Response(director_serializer.data, status=status.HTTP_201_CREATED)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def manage_single_director(request, pk):
    director = Director.objects.filter(id=pk)
    if not director.exists():
        return Response({"error": "Director does not exist"}, status=status.HTTP_400_BAD_REQUEST)
    serializer = DirectorSerializer(director, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Zarządzanie administratorami
@api_view(['GET', 'POST'])
def manage_admins(request):
    if request.method == 'GET':
        admins = Admin.objects.all()
        serializer = AdminSerializer(admins, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        user_serializer = CustomUserSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save(user_type='Administrator')  # Domyślnie typ użytkownika ustawiony na "Administrator"
            admin = Admin.objects.create(user=user)
            admin_serializer = AdminSerializer(admin)
            return Response(admin_serializer.data, status=status.HTTP_201_CREATED)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def manage_single_admin(request, pk):
    admin = Admin.objects.filter(id=pk)
    if not admin.exists():
        return Response({"error": "Admin does not exist"}, status=status.HTTP_400_BAD_REQUEST)
    serializer = AdminSerializer(admin, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)