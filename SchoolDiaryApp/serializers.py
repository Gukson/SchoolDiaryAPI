from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from SchoolDiaryApp.models import Director, Teacher, CustomUser, Parent, Student
from SchoolDiaryApp.models_directory.structures import School
from SchoolDiaryApp.models_directory.structures import Class, Grate, Subject, Classes, Message, Frequency, Announcements


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ['id', 'name']



class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id', 'pesel', 'login', 'Name', 'Surname', 'password',
            'birth_date', 'user_type', 'username', 'email'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

class DirectorSerializer(serializers.ModelSerializer):
    school = SchoolSerializer()
    user = CustomUserSerializer()

    class Meta:
        model = Director
        fields = ['id', 'school', 'user']


class TeacherSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Teacher
        fields = ['id', 'user', 'school']


class AdminSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = CustomUser
        fields = ['id', 'user']


class ParentSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Parent
        fields = ['id', 'user']


class ClassSerializer(serializers.ModelSerializer):
    # Dodanie `write_only=True` dla pola `school`, aby akceptowało tylko ID
    school = serializers.PrimaryKeyRelatedField(
        queryset=School.objects.all(),
        write_only=True
    )
    school_name = serializers.CharField(source='school.name', read_only=True)  # Czytelne wyjście dla API


    class Meta:
        model = Class
        fields = ['id', 'name', 'school', 'school_name', 'supervising_teacher']

class StudentSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    parent = ParentSerializer()

    class Meta:
        model = Student
        fields = ['id', 'user', 'parent', 'school', 'class_id']

from rest_framework import serializers



class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grate
        fields = ['id', 'value', 'weight', 'category', 'description']

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'school']


class ClassesSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer()
    subject = SubjectSerializer()
    class Meta:
        model = Classes
        fields = ['id', 'date', 'lesson_num','time', 'class_id', 'subject', 'teacher']

    class_id = serializers.PrimaryKeyRelatedField(
        queryset=Class.objects.all(),
        required=True
    )



class MessageSerializer(serializers.ModelSerializer):
    sender = CustomUserSerializer()
    address = CustomUserSerializer()
    class Meta:
        model = Message
        fields = ['id', 'date', 'topic', 'content', 'read', 'sender', 'address']


class FrequencySerializer(serializers.ModelSerializer):
    class_id = ClassesSerializer()
    class Meta:
        model = Frequency
        fields = ['id', 'type', 'student', 'class_id']


class StudentWithFrequencySerializer(serializers.ModelSerializer):
    frequencies = FrequencySerializer(many=True, source='students_frequency')
    class Meta:
        model = Student
        fields = ['id', 'user', 'frequencies']

class StudentWithGradesSerializer(serializers.ModelSerializer):
    grades = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ['id', 'user', 'grades']
        depth = 1

    def get_grades(self, obj):
        # Pobierz klasę i przedmiot z kontekstu
        class_ = self.context.get('class_')
        subject = class_.subject if class_ else None

        # Filtrowanie ocen na podstawie przedmiotu i klasy
        if subject:
            grades = obj.grades.filter(class_id=class_, class_id__subject=subject)
        else:
            grades = obj.grades.all()

        # Serializacja ocen
        return GradeSerializer(grades, many=True).data

class SubjectWithGradesSerializer(serializers.Serializer):
    subject = SubjectSerializer()  # Serializuje pojedynczy przedmiot
    grades = GradeSerializer(many=True)  # Serializuje listę ocen

    @staticmethod
    def from_subject_and_grades(subject, grades):
        return {
            "subject": SubjectSerializer(subject).data,
            "grades": GradeSerializer(grades, many=True).data
        }


class GroupedGradesSerializer(serializers.Serializer):
    grouped_grades = serializers.SerializerMethodField()

    def get_grouped_grades(self, instance):
        if not isinstance(instance, Student):
            raise ValueError("The instance must be of type 'Student'.")

        # Pobierz szkołę ucznia
        school = instance.class_id.school

        # Pobierz wszystkie przedmioty w tej szkole
        subjects = Subject.objects.filter(school=school)

        # Pobierz oceny ucznia
        grades = Grate.objects.filter(student=instance)

        # Grupuj oceny według przedmiotu
        grouped_grades = {subject.id: [] for subject in subjects}
        for grade in grades:
            subject_id = grade.class_id.subject.id
            if subject_id in grouped_grades:
                grouped_grades[subject_id].append(grade)

        # Przygotuj wynik za pomocą SubjectWithGradesSerializer
        result = [
            SubjectWithGradesSerializer.from_subject_and_grades(
                subject=subject,
                grades=grouped_grades.get(subject.id, [])
            )
            for subject in subjects
        ]

        return result



class AnnouncementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcements
        fields = ['id', 'topic', 'content', 'date', 'school', 'author']

