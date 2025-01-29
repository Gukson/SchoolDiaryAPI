from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from SchoolDiaryApp.models_directory.structures import Classes, Frequency
from SchoolDiaryApp.models import Teacher, Student
from SchoolDiaryApp.serializers import StudentWithFrequencySerializer, FrequencySerializer
from SchoolDiaryApp.permissions import IsTeacher, IsStudent

@api_view(['GET'])
@permission_classes([IsStudent])
def get_student_frequency(request):
    # Pobierz ucznia na podstawie aktualnie zalogowanego użytkownika
    student = get_object_or_404(Student, user=request.user)

    # Pobierz listę obiektów frekwencji dla ucznia
    frequencies = Frequency.objects.filter(student=student)

    # Serializuj listę obiektów frekwencji
    serializer = FrequencySerializer(frequencies, many=True)

    # Zwróć zserializowane dane jako odpowiedź JSON
    return Response(serializer.data, status=status.HTTP_200_OK)