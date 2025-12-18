from rest_framework import serializers
from .models import Student
from authentication.serializers import UserSerializer


class StudentSerializer(serializers.ModelSerializer):
    """Serializer for Student model"""
    
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Student
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class StudentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating student profile"""
    
    class Meta:
        model = Student
        exclude = ['user', 'created_at', 'updated_at', 'profile_completed']
    
    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        student = Student.objects.create(**validated_data)
        return student


class StudentUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating student profile"""
    
    class Meta:
        model = Student
        exclude = ['user', 'roll_number', 'created_at', 'updated_at']
