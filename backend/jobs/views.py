from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.utils import timezone
from .models import Job, Application, Interview
from .serializers import (JobSerializer, JobCreateSerializer, 
                          ApplicationSerializer, ApplicationCreateSerializer,
                          InterviewSerializer)
from students.models import Student


class JobListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = JobSerializer
    
    def get_queryset(self):
        queryset = Job.objects.filter(is_active=True)
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(Q(title__icontains=search) | Q(recruiter__company_name__icontains=search))
        job_type = self.request.query_params.get('job_type', None)
        if job_type:
            queryset = queryset.filter(job_type=job_type)
        return queryset.order_by('-posted_at')
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return JobCreateSerializer
        return JobSerializer


class JobDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = JobSerializer
    queryset = Job.objects.all()
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views_count += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class StudentApplicationView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, job_id):
        try:
            student = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            return Response({'error': 'Please complete your profile first'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            job = Job.objects.get(id=job_id, is_active=True)
        except Job.DoesNotExist:
            return Response({'error': 'Job not found'}, status=status.HTTP_404_NOT_FOUND)
        if Application.objects.filter(student=student, job=job).exists():
            return Response({'error': 'Already applied'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ApplicationCreateSerializer(data=request.data, context={'student': student, 'job': job})
        if serializer.is_valid():
            application = serializer.save()
            return Response(ApplicationSerializer(application).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyApplicationsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ApplicationSerializer
    
    def get_queryset(self):
        try:
            student = Student.objects.get(user=self.request.user)
            return Application.objects.filter(student=student).order_by('-applied_at')
        except Student.DoesNotExist:
            return Application.objects.none()
