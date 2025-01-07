from rest_framework import serializers

from SchoolDiaryApp.models import Director, Teacher, CustomUser, Parent, Student
from SchoolDiaryApp.models_directory.structures import School
from SchoolDiaryApp.models_directory.structures import Class, Grate, Subject, Classes, Message, Frequency


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ['id', 'name']


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id', 'pesel', 'login', 'Name', 'Surname',
            'birth_date', 'user_type', 'username', 'email'
        ]


class DirectorSerializer(serializers.ModelSerializer):
    schoolID = SchoolSerializer()
    user = CustomUserSerializer()

    class Meta:
        model = Director
        fields = ['id', 'schoolID', 'user']


class TeacherSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Teacher
        fields = ['id', 'user']


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
        model = CustomUser
        fields = ['id', 'user', 'parent']

from rest_framework import serializers
from collections import defaultdict



class GroupedGradesSerializer(serializers.Serializer):
    subject = serializers.CharField()
    scores = serializers.ListField(child=serializers.DecimalField(max_digits=5, decimal_places=2))

    @staticmethod
    def group_by_subject(grades):
        grouped = defaultdict(list)
        for grade in grades:
            subject_name = grade.class_id.subject  # Pobieramy nazwę przedmiotu z class_id.subject
            grouped[subject_name].append(grade.score)
        return grouped

    def to_representation(self, instance):
        grouped_grades = self.group_by_subject(instance)
        result = []
        for subject, grade_objects in grouped_grades.items():
            serialized_grades = GradeSerializer(grade_objects, many=True).data
            result.append({
                "subject": subject,
                "grades": serialized_grades
            })
        return result


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