from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from SchoolDiaryApp.models import Grate
from SchoolDiaryApp.permissions import IsStudent
from SchoolDiaryApp.serializers import GroupedGradesSerializer
from django.shortcuts import get_object_or_404
from SchoolDiaryApp.models import Student


@api_view(['GET'])
def get_grouped_grades(request):
    # Pobierz studenta na podstawie aktualnie zalogowanego użytkownika
    student = get_object_or_404(Student, user=request.user)

    # Przekaż instancję studenta do serializatora
    serializer = GroupedGradesSerializer()
    serialized_data = serializer.to_representation(student)

    # Zwróć zserializowane dane jako odpowiedź
    return Response(serialized_data)