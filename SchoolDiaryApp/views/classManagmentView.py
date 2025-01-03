
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

from ..models_directory.structures import Class, School
from ..serializers import ClassSerializer


@api_view(['GET', 'POST'])
def classes_view(request, school_id):
    try:
        school = School.objects.get(id=school_id)
    except School.DoesNotExist:
        return Response({'error': 'School not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        classes = Class.objects.filter(school=school)
        serializer = ClassSerializer(classes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        data = request.data
        data['school'] = school.id  # Automatycznie ustaw ID szkoły w danych

        serializer = ClassSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
