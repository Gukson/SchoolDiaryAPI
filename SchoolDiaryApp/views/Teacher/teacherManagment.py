from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from SchoolDiaryApp.models import Teacher, Director
from SchoolDiaryApp.serializers import TeacherSerializer, CustomUserSerializer
from rest_framework.decorators import api_view, permission_classes


# Zarządzanie nauczycielami

@api_view(['GET','POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def manage_teachers(request):
    user = request.user
    if request.method == 'GET':
        teachers = Teacher.objects.all()
        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST' and user.groups.filter(name='Director').exists():
        director = Director.objects.get(user=user)
        user_serializer = CustomUserSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save(user_type='Teacher')  # Domyślnie typ użytkownika ustawiony na "Teacher"
            teacher = Teacher.objects.create(user=user, school=director.school)
            teacher_serializer = TeacherSerializer(teacher)
            return Response(teacher_serializer.data, status=status.HTTP_201_CREATED)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE' and user.groups.filter(name='Director').exists():
        teacher_id = request.data.get('teacher_id')
        teacher = Teacher.objects.filter(id=teacher_id)
        teacher.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
