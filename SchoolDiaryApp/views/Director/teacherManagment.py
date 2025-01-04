from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from SchoolDiaryApp.models import Teacher
from SchoolDiaryApp.serializers import TeacherSerializer, CustomUserSerializer
from rest_framework.decorators import api_view, permission_classes
from SchoolDiaryApp.permissions import IsDirector

# Zarządzanie nauczycielami

@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsDirector])
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
    elif request.method == 'DELETE':
        teacher_id = request.data.get('id')
        teacher = Teacher.objects.filter(id=teacher_id)
        teacher.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsDirector])
def manage_single_teacher(request, pk):
    teacher = Teacher.objects.filter(id=pk)
    if not teacher.exists():
        return Response({"error": "Teacher does not exist"}, status=status.HTTP_400_BAD_REQUEST)
    serializer = TeacherSerializer(teacher, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)