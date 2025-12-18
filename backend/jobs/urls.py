from django.urls import path
from .views import (JobListCreateView, JobDetailView, StudentApplicationView, MyApplicationsView)
from .interview_views import (ScheduleInterviewView, StudentInterviewsView, InterviewDetailView)

urlpatterns = [
    path('', JobListCreateView.as_view(), name='job-list-create'),
    path('<int:pk>/', JobDetailView.as_view(), name='job-detail'),
    path('<int:job_id>/apply/', StudentApplicationView.as_view(), name='job-apply'),
    path('applications/my/', MyApplicationsView.as_view(), name='my-applications'),
    
    # Interview endpoints
    path('interviews/schedule/', ScheduleInterviewView.as_view(), name='schedule-interview'),
    path('interviews/my/', StudentInterviewsView.as_view(), name='my-interviews'),
    path('interviews/<int:pk>/', InterviewDetailView.as_view(), name='interview-detail'),
]
