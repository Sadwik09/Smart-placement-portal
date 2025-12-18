"""
ML Integration Views
Connects ML modules (skill matcher, recommender, resume scorer) with Django REST API
"""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from students.models import Student
from recruiters.models import Recruiter
from jobs.models import Job, Application
from resumes.models import Resume
from placement_portal.permissions import IsStudent, IsRecruiter
import os
import sys

# Add ML modules to path
sys.path.append(os.path.join(settings.BASE_DIR.parent, 'ml_modules'))

try:
    from skill_matcher.matcher import SkillMatcher
    from recommender.engine import RecommendationEngine
    from resume_scorer.scorer import ResumeScorer
except ImportError as e:
    SkillMatcher = None
    RecommendationEngine = None
    ResumeScorer = None
    print(f"ML modules import error: {e}")


class JobRecommendationsView(APIView):
    """Get AI-powered job recommendations for student"""
    permission_classes = [IsAuthenticated, IsStudent]
    
    def get(self, request):
        try:
            student = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            return Response({'error': 'Student profile not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if not RecommendationEngine:
            return Response({'error': 'ML engine not available'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
        # Get student skills
        student_skills = student.skills or []
        if not student_skills:
            return Response({
                'message': 'No skills found. Please update your profile with skills.',
                'recommendations': []
            })
        
        # Get active jobs
        jobs = Job.objects.filter(is_active=True)
        
        # Prepare job data
        job_data = []
        for job in jobs:
            job_data.append({
                'id': job.id,
                'title': job.title,
                'company_name': job.company_name,
                'location': job.location,
                'ctc': job.ctc,
                'job_type': job.job_type,
                'skills_required': job.skills_required or [],
                'min_cgpa': float(job.min_cgpa) if job.min_cgpa else 0,
                'deadline': job.deadline.isoformat()
            })
        
        # Get recommendations
        engine = RecommendationEngine()
        recommendations = engine.recommend_jobs(student_skills, job_data, student.cgpa or 0)
        
        # Filter by CGPA
        filtered_recs = [rec for rec in recommendations if rec['match_score'] >= 30]
        
        return Response({
            'student_skills': student_skills,
            'total_jobs': len(jobs),
            'recommendations': filtered_recs[:10]  # Top 10
        })


class CandidateRecommendationsView(APIView):
    """Get AI-powered candidate recommendations for recruiter's job"""
    permission_classes = [IsAuthenticated, IsRecruiter]
    
    def get(self, request, job_id):
        try:
            job = Job.objects.get(id=job_id, posted_by__user=request.user)
        except Job.DoesNotExist:
            return Response({'error': 'Job not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if not RecommendationEngine:
            return Response({'error': 'ML engine not available'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
        # Get job skills
        job_skills = job.skills_required or []
        if not job_skills:
            return Response({
                'message': 'No skills required for this job.',
                'recommendations': []
            })
        
        # Get all students meeting CGPA requirement
        students = Student.objects.filter(
            user__is_approved=True,
            cgpa__gte=job.min_cgpa
        )
        
        # Prepare student data
        student_data = []
        for student in students:
            student_data.append({
                'id': student.id,
                'name': student.user.get_full_name(),
                'email': student.user.email,
                'roll_number': student.roll_number,
                'branch': student.branch,
                'cgpa': float(student.cgpa) if student.cgpa else 0,
                'skills': student.skills or []
            })
        
        # Get recommendations
        engine = RecommendationEngine()
        recommendations = engine.recommend_candidates(job_skills, student_data)
        
        # Filter high matches
        filtered_recs = [rec for rec in recommendations if rec['match_score'] >= 40]
        
        return Response({
            'job_title': job.title,
            'required_skills': job_skills,
            'total_students': len(students),
            'recommendations': filtered_recs[:20]  # Top 20
        })


class CalculateMatchScoreView(APIView):
    """Calculate match score between student and job"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        job_id = request.data.get('job_id')
        student_id = request.data.get('student_id')
        
        if not job_id or not student_id:
            return Response({'error': 'job_id and student_id are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            job = Job.objects.get(id=job_id)
            student = Student.objects.get(id=student_id)
        except (Job.DoesNotExist, Student.DoesNotExist):
            return Response({'error': 'Job or Student not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if not SkillMatcher:
            return Response({'error': 'ML matcher not available'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
        # Get skills
        job_skills = job.skills_required or []
        student_skills = student.skills or []
        
        if not job_skills or not student_skills:
            return Response({
                'match_score': 0,
                'message': 'Insufficient skill data for matching'
            })
        
        # Calculate match
        matcher = SkillMatcher()
        match_result = matcher.calculate_match_detailed(student_skills, job_skills)
        
        return Response({
            'match_score': match_result['match_score'],
            'matched_skills': match_result['matched_skills'],
            'missing_skills': match_result['missing_skills'],
            'extra_skills': match_result['extra_skills'],
            'cgpa_eligible': student.cgpa >= job.min_cgpa if student.cgpa and job.min_cgpa else True
        })


class ResumeScoreView(APIView):
    """Get resume score and analysis"""
    permission_classes = [IsAuthenticated, IsStudent]
    
    def get(self, request, resume_id=None):
        try:
            student = Student.objects.get(user=request.user)
            
            if resume_id:
                resume = Resume.objects.get(id=resume_id, student=student)
            else:
                # Get active resume
                resume = Resume.objects.filter(student=student, is_active=True).first()
                
            if not resume:
                return Response({'error': 'No resume found'}, status=status.HTTP_404_NOT_FOUND)
            
            if not resume.is_parsed or not resume.parsed_text:
                return Response({'error': 'Resume not yet parsed'}, status=status.HTTP_400_BAD_REQUEST)
            
            if not ResumeScorer:
                return Response({'error': 'ML scorer not available'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
            
            # Score resume
            scorer = ResumeScorer()
            score_result = scorer.score_resume(resume.parsed_text)
            
            return Response({
                'resume_id': resume.id,
                'overall_score': score_result['overall_score'],
                'breakdown': score_result['breakdown'],
                'recommendations': score_result['recommendations'],
                'uploaded_at': resume.uploaded_at
            })
            
        except Student.DoesNotExist:
            return Response({'error': 'Student profile not found'}, status=status.HTTP_404_NOT_FOUND)
        except Resume.DoesNotExist:
            return Response({'error': 'Resume not found'}, status=status.HTTP_404_NOT_FOUND)
