from django.shortcuts import render


# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

from ..models import School
from ..permissions import *
from ..serializers import SchoolSerializer


@api_view(['GET', 'POST'])
@permission_classes(IsAdministrator)
def school_view(request):
    if request.method == 'POST':
        school_name = request.data['schoolName']
        if not school_name:
            return Response({'error': 'School Name is required'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = SchoolSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        schools = School.objects.all()
        serializer = SchoolSerializer(schools, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

