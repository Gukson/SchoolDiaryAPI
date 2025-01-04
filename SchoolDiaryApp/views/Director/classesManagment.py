from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from datetime import timedelta, datetime
from SchoolDiaryApp.models_directory.structures import Classes, Class, Subject
from SchoolDiaryApp.models import Teacher, Director
from SchoolDiaryApp.serializers import SubjectSerializer, ClassSerializer, ClassesSerializer
from SchoolDiaryApp.permissions import IsDirector

@api_view(['GET','POST'])
@permission_classes([IsDirector])
def create_recurring_classes(request):
    """
    Tworzy zajęcia cyklicznie (co tydzień lub co dwa tygodnie) w podanym przedziale czasowym.
    """
    if request.method == 'POST':
        data = request.data

        # Walidacja pól wejściowych
        class_name = data.get('class_name')
        subject_id = data.get('subject_id')
        teacher_id = data.get('teacher_id')
        start_date = data.get('start_date')  # Format: YYYY-MM-DD
        end_date = data.get('end_date')  # Format: YYYY-MM-DD
        start_time = data.get('start_time')  # Format: HH:MM:SS
        lesson_num = data.get('lesson_num')
        frequency = data.get('frequency')  # 1 = co tydzień, 2 = co dwa tygodnie

        # Walidacja podstawowych pól
        if not all([class_name, subject_id, teacher_id, start_date, end_date, start_time, frequency]):
            return Response(
                {
                    "error": "Wszystkie pola (class_name, subject_id, teacher_id, start_date, end_date, start_time, frequency) są wymagane."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Walidacja częstotliwości
        if frequency not in [1, 2]:
            return Response({"error": "Częstotliwość może być tylko 1 (co tydzień) lub 2 (co dwa tygodnie)."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Konwersja dat
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            start_time = datetime.strptime(start_time, '%H:%M').time()
        except ValueError:
            return Response({"error": "Nieprawidłowy format daty lub godziny. Użyj formatów YYYY-MM-DD i HH:MM:SS."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Pobranie obiektów z bazy danych
        class_obj = get_object_or_404(Class, name=class_name)
        subject_obj = get_object_or_404(Subject, id=subject_id)
        teacher_obj = get_object_or_404(Teacher, id=teacher_id)

        # Walidacja: Czy użytkownik jest przypisany jako dyrektor szkoły tej klasy

        # Tworzenie zajęć cyklicznie
        current_date = start_date
        created_classes = []

        while current_date <= end_date:
            new_class = Classes.objects.create(
                date=current_date,
                time=start_time,  # Dodanie godziny
                lesson_num=lesson_num,  # Możesz to dostosować
                class_id=class_obj,
                subject=subject_obj,
                teacher=teacher_obj
            )
            created_classes.append(new_class)
            current_date += timedelta(weeks=frequency)

        # Serializacja wyników
        return Response(
            {"message": f"Utworzono {len(created_classes)} zajęć cyklicznych."},
            status=status.HTTP_201_CREATED
        )
    elif request.method == 'GET':
        classes = Classes.objects.all()
        serializer = ClassesSerializer(classes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
@permission_classes([IsDirector])  # Dostęp tylko dla dyrektorów
def subject_view(request):
    director = get_object_or_404(Director, user=request.user)
    school = director.school
    if request.method == "POST":
        subject_name = request.data.get('name')

        # Walidacja
        if not subject_name:
            return Response({"error": "Pole 'name' jest wymagane."}, status=status.HTTP_400_BAD_REQUEST)

        # Sprawdzenie, czy przedmiot już istnieje w danej szkole
        if Subject.objects.filter(name=subject_name, school=school).exists():
            return Response(
                {"error": f"Przedmiot o nazwie '{subject_name}' już istnieje w tej szkole."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Tworzenie nowego przedmiotu
        serializer = SubjectSerializer(data=request.data)
        if serializer.is_valid():
            subject = Subject.objects.create(name=subject_name, school=school)
            serialized_subject = SubjectSerializer(subject)
            return Response(serialized_subject.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "GET":
        # Pobierz przedmioty tylko dla szkoły zalogowanego dyrektora
        subjects = Subject.objects.filter(school=school)
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)