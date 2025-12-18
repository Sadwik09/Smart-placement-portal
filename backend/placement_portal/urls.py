"""
URL configuration for placement_portal project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .ml_views import (
    JobRecommendationsView,
    CandidateRecommendationsView,
    CalculateMatchScoreView,
    ResumeScoreView
)
from .health_views import HealthCheckView

urlpatterns = [
    path('health/', HealthCheckView.as_view(), name='health-check'),
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),
    path('api/students/', include('students.urls')),
    path('api/recruiters/', include('recruiters.urls')),
    path('api/jobs/', include('jobs.urls')),
    path('api/resumes/', include('resumes.urls')),
    path('api/analytics/', include('analytics.urls')),
    
    # ML Integration endpoints
    path('api/ml/job-recommendations/', JobRecommendationsView.as_view(), name='job-recommendations'),
    path('api/ml/candidate-recommendations/<int:job_id>/', CandidateRecommendationsView.as_view(), name='candidate-recommendations'),
    path('api/ml/calculate-match/', CalculateMatchScoreView.as_view(), name='calculate-match'),
    path('api/ml/resume-score/', ResumeScoreView.as_view(), name='resume-score'),
    path('api/ml/resume-score/<int:resume_id>/', ResumeScoreView.as_view(), name='resume-score-detail'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
