from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from SchoolDiaryApp.models_directory.structures import Classes
from SchoolDiaryApp.models import Teacher
from SchoolDiaryApp.serializers import  ClassesSerializer
from SchoolDiaryApp.permissions import  IsTeacher
from datetime import datetime


@api_view(['GET'])
@permission_classes([IsTeacher])
def get_teacher_classes(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    date = request.data.get('date')
    parsed_date = datetime.strptime(date, '%Y-%m-%d').date()

    classes = Classes.objects.filter(teacher=teacher, date=parsed_date).order_by('lesson_number')
    serializer = ClassesSerializer(classes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)