from rest_framework import serializers

from SchoolDiaryApp.models import Director, Teacher, CustomUser, Parent, Student
from SchoolDiaryApp.models_directory.structures import School
from SchoolDiaryApp.models_directory.structures import Class, Grate, Subject, Classes, Message, Frequency, Announcements


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ['id', 'name']

from SchoolDiaryApp.serializers import *

class CustomUserSerializer(serializers.ModelSerializer):
    student = StudentSerializer()
    teacher = TeacherSerializer()
    director = DirectorSerializer()
    parent = ParentSerializer()

    class Meta:
        model = CustomUser
        fields = [
            'id', 'pesel', 'login', 'Name', 'Surname',
            'birth_date', 'user_type', 'username', 'email',
            'student', 'teacher', 'director', 'parent'
        ]

    def get_student(self, obj):
        if hasattr(obj, 'student'):
            return StudentSerializer(obj.student).data
        return None

    def get_teacher(self, obj):
        if hasattr(obj, 'teacher'):
            return TeacherSerializer(obj.teacher).data
        return None

    def get_director(self, obj):
        if hasattr(obj, 'director'):
            return DirectorSerializer(obj.director).data
        return None

    def get_parent(self, obj):
        if hasattr(obj, 'parent'):
            return ParentSerializer(obj.parent).data
        return None


class DirectorSerializer(serializers.ModelSerializer):
    schoolID = SchoolSerializer()
    user = CustomUserSerializer()

    class Meta:
        model = Director
        fields = ['id', 'schoolID', 'user']


class TeacherSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    schoolID = SchoolSerializer()

    class Meta:
        model = Teacher
        fields = ['id', 'user', 'schoolID']


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