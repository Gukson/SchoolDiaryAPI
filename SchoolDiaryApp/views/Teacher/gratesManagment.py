from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from SchoolDiaryApp.models_directory.structures import Classes, Grate
from SchoolDiaryApp.models import Teacher, Student
from SchoolDiaryApp.serializers import StudentWithGradesSerializer
from SchoolDiaryApp.permissions import IsTeacher, IsStudent


@api_view(['POST'])
@permission_classes([IsTeacher])
def class_grates(request):
    if request.method == 'POST':
        data = request.data
        class_id = data.get('classes_id')

        if not class_id  or 'grates' not in data:
            return Response(
                {"error": "classes_id is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Pobierz klasę
        class_ = get_object_or_404(Classes, id=class_id)

        created_grates = []
        for student_info in data['grates']:
            student_id = student_info.get('student_id')
            value = student_info.get('value')
            weight = student_info.get('weight')
            category = student_info.get('category')
            description = student_info.get('description')

            # Walidacja obecności pól
            if not student_id or not value or not weight or not category or not description:
                return Response(
                    {"error": "Each grate entry must include student_id and type."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Pobierz studenta
            student = get_object_or_404(Student, id=student_id)

            # Utwórz obiekt Frequency
            new_grate = Grate.objects.create(
                value=value,
                weight=weight,
                category=category,
                description=description,
                class_id=class_,
                student=student
            )
            created_grates.append(new_grate)

        # Zwróć informacje o utworzonych frekwencjach
        # serializer = StudentWithGradesSerializer(created_grates, many=True)
        return Response(status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsTeacher])
def class_grate_get(request):
    data = request.data
    class_id = data.get('classes_id')

    if not class_id:
        return Response({"error": "Parameter 'classes_id' is required."}, status=status.HTTP_400_BAD_REQUEST)

    # Pobierz klasę
    class_ = get_object_or_404(Classes, id=class_id)

    # Pobierz uczniów należących do tej klasy
    students = Student.objects.filter(class_id=class_.class_id)

    # Serializacja uczniów wraz z ocenami
    serializer = StudentWithGradesSerializer(students, many=True, context={'class_': class_})
    return Response(serializer.data, status=status.HTTP_200_OK)