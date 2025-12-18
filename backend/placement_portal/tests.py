"""
Test suite for ML endpoints
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from authentication.models import User
from students.models import Student
from jobs.models import Job
from recruiters.models import Recruiter

class RecommendationTestCase(TestCase):
    """Test ML recommendation endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        # Create student
        student_user = User.objects.create_user(
            email='student@example.com',
            password='testpass123',
            first_name='John',
            last_name='Student',
            role='student'
        )
        self.student = Student.objects.create(
            user=student_user,
            roll_number='CS2021001',
            branch='CSE',
            cgpa=8.5,
            year=4
        )
        self.client.force_authenticate(user=student_user)
    
    def test_get_job_recommendations(self):
        """Test getting job recommendations"""
        url = reverse('job-recommendations')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('student_skills', response.data)
        self.assertIn('recommendations', response.data)
    
    def test_recommendations_returns_jobs(self):
        """Test that recommendations include job objects"""
        # Create a job first
        recruiter_user = User.objects.create_user(
            email='recruiter@company.com',
            password='testpass123',
            first_name='Jane',
            last_name='Recruiter',
            role='recruiter'
        )
        recruiter = Recruiter.objects.create(
            user=recruiter_user,
            company_name='TechCorp',
            company_website='https://techcorp.com'
        )
        Job.objects.create(
            recruiter=recruiter,
            title='Python Developer',
            location='Bangalore',
            job_type='full_time'
        )
        
        url = reverse('job-recommendations')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class MatchScoreTestCase(TestCase):
    """Test match score calculation"""
    
    def setUp(self):
        self.client = APIClient()
        # Create student
        student_user = User.objects.create_user(
            email='student@example.com',
            password='testpass123',
            first_name='John',
            last_name='Student',
            role='student'
        )
        self.student = Student.objects.create(
            user=student_user,
            roll_number='CS2021001',
            branch='CSE',
            cgpa=8.5,
            year=4
        )
        
        # Create job
        recruiter_user = User.objects.create_user(
            email='recruiter@company.com',
            password='testpass123',
            first_name='Jane',
            last_name='Recruiter',
            role='recruiter'
        )
        recruiter = Recruiter.objects.create(
            user=recruiter_user,
            company_name='TechCorp',
            company_website='https://techcorp.com'
        )
        self.job = Job.objects.create(
            recruiter=recruiter,
            title='Python Developer',
            location='Bangalore',
            job_type='full_time'
        )
        self.client.force_authenticate(user=recruiter_user)
    
    def test_calculate_match_score(self):
        """Test calculating match score"""
        data = {
            'job_id': self.job.id,
            'student_id': self.student.id
        }
        url = reverse('calculate-match')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('match_score', response.data)
        # Score should be between 0-100
        self.assertGreaterEqual(response.data['match_score'], 0)
        self.assertLessEqual(response.data['match_score'], 100)
    
    def test_match_score_nonexistent_job(self):
        """Test match score with non-existent job"""
        data = {
            'job_id': 999,
            'student_id': self.student.id
        }
        url = reverse('calculate-match')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
