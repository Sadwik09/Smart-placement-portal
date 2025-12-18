from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import models
from .models import Student
from .serializers import StudentSerializer, StudentCreateSerializer, StudentUpdateSerializer


class StudentProfileView(APIView):
    """Get or create student profile"""
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            student = Student.objects.get(user=request.user)
            serializer = StudentSerializer(student)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            return Response({'error': 'Profile not found. Please create your profile.'}, status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request):
        if hasattr(request.user, 'student_profile'):
            return Response({'error': 'Profile already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = StudentCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            student = serializer.save()
            return Response(StudentSerializer(student).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        try:
            student = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = StudentUpdateSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(StudentSerializer(student).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentListView(generics.ListAPIView):
    """List all students (for recruiters/admin)"""
    
    permission_classes = [IsAuthenticated]
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    
    def get_queryset(self):
        queryset = Student.objects.all()
        branch = self.request.query_params.get('branch', None)
        if branch:
            queryset = queryset.filter(branch=branch)
        year = self.request.query_params.get('year', None)
        if year:
            queryset = queryset.filter(year=year)
        min_cgpa = self.request.query_params.get('min_cgpa', None)
        if min_cgpa:
            queryset = queryset.filter(cgpa__gte=min_cgpa)
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(models.Q(name__icontains=search) | models.Q(roll_number__icontains=search))
        return queryset
