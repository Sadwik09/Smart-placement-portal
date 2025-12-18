"""
Interview Management Views
"""
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from jobs.models import Interview, Application
from placement_portal.permissions import IsRecruiter, IsStudent
from rest_framework import serializers


class InterviewSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='application.student.user.get_full_name', read_only=True)
    job_title = serializers.CharField(source='application.job.title', read_only=True)
    company = serializers.CharField(source='application.job.company_name', read_only=True)
    
    class Meta:
        model = Interview
        fields = '__all__'
        read_only_fields = ['application', 'created_at']


class ScheduleInterviewView(generics.CreateAPIView):
    """Schedule interview for an application (Recruiter only)"""
    serializer_class = InterviewSerializer
    permission_classes = [IsAuthenticated, IsRecruiter]
    
    def create(self, request, *args, **kwargs):
        application_id = request.data.get('application_id')
        
        try:
            application = Application.objects.get(id=application_id)
            
            # Check if recruiter owns this job
            if application.job.posted_by.user != request.user:
                return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
            
            # Create interview
            interview = Interview.objects.create(
                application=application,
                scheduled_date=request.data.get('scheduled_date'),
                scheduled_time=request.data.get('scheduled_time'),
                mode=request.data.get('mode', 'online'),
                location=request.data.get('location', ''),
                meeting_link=request.data.get('meeting_link', ''),
                interviewer_name=request.data.get('interviewer_name', ''),
                interviewer_email=request.data.get('interviewer_email', ''),
                notes=request.data.get('notes', '')
            )
            
            # Update application status
            application.status = 'interview_scheduled'
            application.save()
            
            serializer = self.get_serializer(interview)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Application.DoesNotExist:
            return Response({'error': 'Application not found'}, status=status.HTTP_404_NOT_FOUND)


class StudentInterviewsView(generics.ListAPIView):
    """Get all interviews for logged-in student"""
    serializer_class = InterviewSerializer
    permission_classes = [IsAuthenticated, IsStudent]
    
    def get_queryset(self):
        return Interview.objects.filter(
            application__student__user=self.request.user
        ).order_by('-scheduled_date', '-scheduled_time')


class InterviewDetailView(generics.RetrieveUpdateAPIView):
    """Get or update interview details"""
    serializer_class = InterviewSerializer
    permission_classes = [IsAuthenticated]
    queryset = Interview.objects.all()
    
    def update(self, request, *args, **kwargs):
        interview = self.get_object()
        
        # Only recruiter can update
        if request.user != interview.application.job.posted_by.user:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        return super().update(request, *args, **kwargs)
