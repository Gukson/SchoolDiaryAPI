from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from SchoolDiaryApp.models import Grate
from SchoolDiaryApp.permissions import IsStudent
from SchoolDiaryApp.serializers import GroupedGradesSerializer
from django.shortcuts import get_object_or_404
from SchoolDiaryApp.models import Student


@api_view(['GET'])
@permission_classes([IsStudent])  # Wymaga zalogowania
def get_student_grades(request):
    student = get_object_or_404(Student, user=request.user)
    grades = Grate.objects.filter(student=student)
    serializer = GroupedGradesSerializer(grades, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)