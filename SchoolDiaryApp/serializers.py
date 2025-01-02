from rest_framework import serializers

from SchoolDiaryApp.models import School, Director, Teacher, CustomUser, Parent, Class, Grate


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
    school = SchoolSerializer()
    supervising_teacher = TeacherSerializer()

    class Meta:
        model = Class
        fields = ['id', 'name', 'school', 'supervising_teacher']


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