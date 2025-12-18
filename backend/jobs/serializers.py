from rest_framework import serializers
from .models import Job, Application, Interview
from students.serializers import StudentSerializer
from recruiters.models import Recruiter


class JobSerializer(serializers.ModelSerializer):
    """Serializer for Job model"""
    
    company_name = serializers.CharField(source='recruiter.company_name', read_only=True)
    company_location = serializers.CharField(source='recruiter.location', read_only=True)
    
    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ['recruiter', 'posted_at', 'updated_at', 'views_count', 'applications_count']


class JobCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating job postings"""
    
    class Meta:
        model = Job
        exclude = ['recruiter', 'posted_at', 'updated_at', 'views_count', 'applications_count']
    
    def create(self, validated_data):
        recruiter = self.context['request'].user.recruiter_profile
        validated_data['recruiter'] = recruiter
        job = Job.objects.create(**validated_data)
        return job


class ApplicationSerializer(serializers.ModelSerializer):
    """Serializer for Application model"""
    
    student = StudentSerializer(read_only=True)
    job = JobSerializer(read_only=True)
    student_name = serializers.CharField(source='student.name', read_only=True)
    student_roll = serializers.CharField(source='student.roll_number', read_only=True)
    job_title = serializers.CharField(source='job.title', read_only=True)
    company_name = serializers.CharField(source='job.recruiter.company_name', read_only=True)
    
    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ['student', 'job', 'applied_at', 'reviewed_at', 'updated_at']


class ApplicationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating job applications"""
    
    class Meta:
        model = Application
        fields = ['cover_letter']
    
    def create(self, validated_data):
        student = self.context['student']
        job = self.context['job']
        validated_data['student'] = student
        validated_data['job'] = job
        application = Application.objects.create(**validated_data)
        
        # Increment application count
        job.applications_count += 1
        job.save()
        
        return application


class InterviewSerializer(serializers.ModelSerializer):
    """Serializer for Interview model"""
    
    student_name = serializers.CharField(source='application.student.name', read_only=True)
    job_title = serializers.CharField(source='application.job.title', read_only=True)
    
    class Meta:
        model = Interview
        fields = '__all__'
        read_only_fields = ['application', 'created_at', 'updated_at']
