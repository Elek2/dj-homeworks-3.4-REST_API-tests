from rest_framework import serializers

from django.conf import settings
from students.models import Course, Student


class StudentSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return Student(**validated_data)

    class Meta:
        model = Student
        fields = ("id", "name")


class CourseSerializer(serializers.ModelSerializer):
    students = StudentSerializer(read_only=True, many=True)

    class Meta:
        model = Course
        fields = ("id", "name", "students")

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        a = len(self.initial_data['students'])
        if a > settings.MAX_STUDENTS_PER_COURSE:
            raise serializers.ValidationError("Максимальное число студентов на курсе — 20")

        return data
