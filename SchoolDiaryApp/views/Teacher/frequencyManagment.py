from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from SchoolDiaryApp.models_directory.structures import Classes, Frequency
from SchoolDiaryApp.models import Teacher, Student
from SchoolDiaryApp.serializers import StudentWithFrequencySerializer, FrequencySerializer
from SchoolDiaryApp.permissions import IsTeacher, IsStudent


@api_view(['POST', 'GET'])
@permission_classes([IsTeacher])
def class_frequency(request):
    if request.method == 'POST':
        data = request.data
        class_id = data.get('class_id')

        if not class_id or 'frequency' not in data:
            return Response(
                {"error": "classes_id and frequency data are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Pobierz klasę
        class_ = get_object_or_404(Classes, id=class_id)

        created_frequencies = []
        for student_info in data['frequency']:
            student_id = student_info.get('student_id')
            frequency_type = student_info.get('type')

            # Walidacja obecności pól
            if not student_id or not frequency_type:
                return Response(
                    {"error": "Each frequency entry must include student_id and type."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Pobierz studenta
            student = get_object_or_404(Student, id=student_id)

            # Utwórz obiekt Frequency
            new_frequency = Frequency.objects.create(
                class_id=class_,
                student=student,
                type=frequency_type
            )
            created_frequencies.append(new_frequency)

        # Zwróć informacje o utworzonych frekwencjach
        serializer = FrequencySerializer(created_frequencies, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsTeacher])
def get_class_frequency(request):
    class_id = request.data.get('class_id')

    if not class_id:
        return Response({"error": "Parameter 'class_id' is required."}, status=status.HTTP_400_BAD_REQUEST)

    # Pobierz klasę
    class_ = get_object_or_404(Classes, id=class_id)

    # Pobierz uczniów w tej klasie
    students = Student.objects.filter(class_id=class_.class_id)

    # Serializuj dane o uczniach i ich frekwencji
    serializer = StudentWithFrequencySerializer(students, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST', 'GET', 'PATCH', 'DELETE'])
@permission_classes([IsTeacher])
def student_frequency(request):
    if request.method == 'POST':
        data = request.data

        # Pobierz student_id, class_id, i type z danych żądania
        student_id = data.get('student_id')
        class_id = data.get('class_id')
        frequency_type = data.get('type')

        # Walidacja obecności wymaganych pól
        if not all([student_id, class_id, frequency_type]):
            return Response(
                {"error": "student_id, class_id, and type are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Pobierz ucznia i klasę
        student = get_object_or_404(Student, id=student_id)
        class_ = get_object_or_404(Classes, id=class_id)

        # Utwórz obiekt Frequency
        new_frequency = Frequency.objects.create(
            class_id=class_,
            student=student,
            type=frequency_type
        )

        # Serializacja nowo utworzonej frekwencji
        serializer = FrequencySerializer(new_frequency)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    elif request.method == 'GET':
        # Pobierz student_id z parametrów URL
        student_id = request.data.get('student_id')

        if not student_id:
            return Response({"error": "Parameter 'student_id' is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Pobierz ucznia
        student = get_object_or_404(Student, id=student_id)

        # Pobierz frekwencję ucznia
        frequencies = Frequency.objects.filter(student=student)

        # Serializacja frekwencji ucznia
        serializer = FrequencySerializer(frequencies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PATCH':
        data = request.data

        # Pobierz frequency_id i type z danych żądania
        frequency_id = data.get('frequency_id')
        new_type = data.get('type')

        # Walidacja obecności wymaganych pól
        if not all([frequency_id, new_type]):
            return Response(
                {"error": "frequency_id and type are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Pobierz obiekt Frequency
        frequency = get_object_or_404(Frequency, id=frequency_id)

        # Zaktualizuj typ frekwencji
        frequency.type = new_type
        frequency.save()

        # Serializacja zaktualizowanego obiektu
        serializer = FrequencySerializer(frequency)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        # Pobierz frequency_id z danych żądania
        frequency_id = request.data.get('frequency_id')

        if not frequency_id:
            return Response({"error": "frequency_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Pobierz obiekt Frequency
        frequency = get_object_or_404(Frequency, id=frequency_id)

        # Usuń obiekt
        frequency.delete()

        return Response({"message": "Frequency deleted successfully."}, status=status.HTTP_204_NO_CONTENT)