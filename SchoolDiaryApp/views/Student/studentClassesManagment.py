from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from SchoolDiaryApp.models_directory.structures import Classes, Class, Subject
from SchoolDiaryApp.models import Student
from SchoolDiaryApp.serializers import  ClassesSerializer
from SchoolDiaryApp.permissions import  IsStudent
from datetime import timedelta
from django.utils.timezone import now

@api_view(['GET'])
@permission_classes([IsStudent])
def get_student_classes(request):
    student = get_object_or_404(Student, user=request.user)
    today = now().date()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    # Filtruj zajęcia
    classes = Classes.objects.filter(
        class_id=student.class_id,
        date__gte=start_of_week,
        date__lte=end_of_week
    )
    serializer = ClassesSerializer(classes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)