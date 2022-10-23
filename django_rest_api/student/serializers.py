from rest_framework import serializers
from .models import Student


class StudentSerializer(serializers.ModelSerializer):
    student_id = serializers.CharField(required=False)
    name = serializers.CharField(required=False)
    age = serializers.CharField(required=False)
    
    class Meta:
        model = Student
        fields = '__all__'