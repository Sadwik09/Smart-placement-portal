"""
Recommendation Engine
Provides job recommendations for students and candidate recommendations for recruiters
"""

from typing import List, Dict
import sys
from pathlib import Path

# Add parent directory to import skill_matcher
sys.path.append(str(Path(__file__).parent.parent))
from skill_matcher.matcher import SkillMatcher


class RecommendationEngine:
    """Generate recommendations using collaborative and content-based filtering"""
    
    def __init__(self):
        """Initialize with skill matcher"""
        self.matcher = SkillMatcher()
    
    def recommend_jobs(self, student_profile: Dict, jobs: List[Dict], top_n: int = 10) -> List[Dict]:
        """
        Recommend top N jobs for a student
        
        Args:
            student_profile: Dict with 'skills', 'cgpa', 'branch', etc.
            jobs: List of job dicts with 'id', 'title', 'skills_required', etc.
            top_n: Number of recommendations to return
        
        Returns:
            List of recommended jobs with match scores
        """
        student_skills = student_profile.get('skills', [])
        
        # Rank all jobs based on skill match
        ranked_jobs = self.matcher.rank_jobs(jobs, student_skills)
        
        # Apply additional filters
        recommendations = []
        for job in ranked_jobs:
            # Calculate recommendation score (weighted)
            rec_score = self._calculate_job_recommendation_score(
                job,
                student_profile
            )
            
            job['recommendation_score'] = rec_score
            recommendations.append(job)
        
        # Re-sort by recommendation score
        recommendations.sort(key=lambda x: x['recommendation_score'], reverse=True)
        
        return recommendations[:top_n]
    
    def recommend_candidates(self, job_details: Dict, candidates: List[Dict], top_n: int = 20) -> List[Dict]:
        """
        Recommend top N candidates for a job
        
        Args:
            job_details: Dict with 'skills_required', 'experience_required', etc.
            candidates: List of student dicts with 'id', 'name', 'skills', etc.
            top_n: Number of candidates to return
        
        Returns:
            List of recommended candidates with match scores
        """
        job_skills = job_details.get('skills_required', [])
        
        # Rank all candidates based on skill match
        ranked_candidates = self.matcher.rank_candidates(candidates, job_skills)
        
        # Apply additional scoring
        recommendations = []
        for candidate in ranked_candidates:
            # Calculate recommendation score
            rec_score = self._calculate_candidate_recommendation_score(
                candidate,
                job_details
            )
            
            candidate['recommendation_score'] = rec_score
            recommendations.append(candidate)
        
        # Re-sort by recommendation score
        recommendations.sort(key=lambda x: x['recommendation_score'], reverse=True)
        
        return recommendations[:top_n]
    
    def _calculate_job_recommendation_score(self, job: Dict, student_profile: Dict) -> float:
        """
        Calculate weighted recommendation score for a job
        Considers skill match, CGPA requirement, etc.
        """
        # Base score from skill match
        skill_match = job.get('match_score', 0)
        
        # Weight: 70% skill match, 30% other factors
        score = skill_match * 0.7
        
        # Add bonus for exact skill matches
        exact_match = job.get('exact_match_percentage', 0)
        score += exact_match * 0.2
        
        # Add bonus if student has many matched skills
        matched_count = job.get('matched_count', 0)
        if matched_count >= 5:
            score += 10
        
        return round(min(score, 100), 2)  # Cap at 100
    
    def _calculate_candidate_recommendation_score(self, candidate: Dict, job_details: Dict) -> float:
        """
        Calculate weighted recommendation score for a candidate
        """
        # Base score from skill match
        skill_match = candidate.get('match_score', 0)
        exact_match = candidate.get('exact_match_percentage', 0)
        
        # Weighted score
        score = (skill_match * 0.6) + (exact_match * 0.4)
        
        return round(min(score, 100), 2)  # Cap at 100
    
    def get_similar_jobs(self, job_id: str, all_jobs: List[Dict], top_n: int = 5) -> List[Dict]:
        """
        Find similar jobs based on skill requirements
        Useful for "Similar Jobs" feature
        """
        target_job = None
        for job in all_jobs:
            if job.get('id') == job_id:
                target_job = job
                break
        
        if not target_job:
            return []
        
        target_skills = target_job.get('skills_required', [])
        similar = []
        
        for job in all_jobs:
            if job.get('id') == job_id:
                continue
            
            match_score = self.matcher.calculate_match(
                job.get('skills_required', []),
                target_skills
            )
            
            similar.append({
                'id': job.get('id'),
                'title': job.get('title'),
                'company': job.get('company'),
                'similarity_score': match_score
            })
        
        # Sort by similarity
        similar.sort(key=lambda x: x['similarity_score'], reverse=True)
        
        return similar[:top_n]


# Example usage
if __name__ == "__main__":
    engine = RecommendationEngine()
    
    # Sample student profile
    student = {
        'id': 1,
        'name': 'John Doe',
        'skills': ['python', 'django', 'sql', 'git'],
        'cgpa': 8.5,
        'branch': 'CSE'
    }
    
    # Sample jobs
    jobs = [
        {
            'id': 1,
            'title': 'Backend Developer',
            'company': 'Tech Corp',
            'skills_required': ['python', 'django', 'postgresql', 'rest api']
        },
        {
            'id': 2,
            'title': 'Full Stack Developer',
            'company': 'StartupX',
            'skills_required': ['javascript', 'react', 'node', 'mongodb']
        }
    ]
    
    # Get recommendations
    recommendations = engine.recommend_jobs(student, jobs, top_n=5)
    
    print("Job Recommendations:")
    for rec in recommendations:
        print(f"{rec['title']} - Score: {rec['recommendation_score']}")
