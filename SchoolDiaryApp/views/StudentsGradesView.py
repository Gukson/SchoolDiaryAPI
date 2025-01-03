from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

from SchoolDiaryApp.models_directory.structures import Grate
from ..permissions import *
from ..serializers import GrateSerializer

@api_view(['GET'])
@permission_classes(IsStudent)
def students_grades_view(request, student_id):
    if request.method == 'GET':
        grates = Grate.objects.filter(student_id=student_id)
        serializer = GrateSerializer(grates, many=True)