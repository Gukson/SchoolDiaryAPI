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
        fields = ['id', 'value', 'weight', 'description', 'class_id', 'category']


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'school']  # Dodajemy również pole `school`, jeśli jest wymagane
        read_only_fields = ['id', 'school']  # `school` będzie tylko do odczytu


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


class GroupedGradesSerializer(serializers.Serializer):
    subject = serializers.CharField()
    grades = serializers.ListField(child=GradeSerializer())

    @staticmethod
    def group_by_subject(subjects, grades):
        grouped = {subject.name: [] for subject in subjects}
        for grade in grades:
            subject_name = grade.class_id.subject.name  # Pobierz nazwę przedmiotu
            if subject_name in grouped:
                grouped[subject_name].append(grade)
        return grouped

    def to_representation(self, instance):
        school = instance.user.school
        subjects = Subject.objects.filter(school=school)
        grades = instance.grades.all()  # Jeśli istnieje relacja `grades` w modelu ucznia
        grouped_grades = self.group_by_subject(subjects, grades)
        result = []
        for subject, grade_objects in grouped_grades.items():
            serialized_grades = GradeSerializer(grade_objects, many=True).data
            result.append({
                "subject": subject,
                "grades": serialized_grades
            })
        return result

class AnnouncementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcements
        fields = ['id', 'topic', 'content', 'date', 'school', 'author']


# class GrateSerializer:
#     pass