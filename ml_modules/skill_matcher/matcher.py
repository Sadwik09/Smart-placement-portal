"""
Skill Matcher Module
Uses TF-IDF and Cosine Similarity to match skills
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import List, Dict


class SkillMatcher:
    """Match student skills with job requirements"""
    
    def __init__(self):
        """Initialize TF-IDF vectorizer"""
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words='english',
            ngram_range=(1, 2)  # Consider unigrams and bigrams
        )
    
    def skills_to_text(self, skills: List[str]) -> str:
        """Convert skills list to text"""
        return ' '.join(skills)
    
    def calculate_match(self, student_skills: List[str], job_skills: List[str]) -> float:
        """
        Calculate match score between student skills and job requirements
        Returns score between 0 and 100
        """
        if not student_skills or not job_skills:
            return 0.0
        
        # Convert skills to text
        student_text = self.skills_to_text(student_skills)
        job_text = self.skills_to_text(job_skills)
        
        try:
            # Create TF-IDF vectors
            tfidf_matrix = self.vectorizer.fit_transform([student_text, job_text])
            
            # Calculate cosine similarity
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            # Convert to percentage
            match_score = round(similarity * 100, 2)
            
            return match_score
        except Exception as e:
            print(f"Error calculating match: {e}")
            return 0.0
    
    def calculate_match_detailed(self, student_skills: List[str], job_skills: List[str]) -> Dict:
        """
        Calculate detailed match information
        Returns dict with match score, matched skills, and missing skills
        """
        # Normalize skills (lowercase for comparison)
        student_skills_lower = [s.lower() for s in student_skills]
        job_skills_lower = [s.lower() for s in job_skills]
        
        # Find matched and missing skills
        matched_skills = list(set(student_skills_lower) & set(job_skills_lower))
        missing_skills = list(set(job_skills_lower) - set(student_skills_lower))
        extra_skills = list(set(student_skills_lower) - set(job_skills_lower))
        
        # Calculate match score
        match_score = self.calculate_match(student_skills, job_skills)
        
        # Calculate match percentage based on exact matches
        exact_match_percentage = 0
        if job_skills_lower:
            exact_match_percentage = round((len(matched_skills) / len(job_skills_lower)) * 100, 2)
        
        return {
            'match_score': match_score,  # TF-IDF based score
            'exact_match_percentage': exact_match_percentage,  # Exact skill overlap
            'matched_skills': matched_skills,
            'missing_skills': missing_skills,
            'extra_skills': extra_skills,
            'total_student_skills': len(student_skills),
            'total_job_skills': len(job_skills),
            'matched_count': len(matched_skills),
            'missing_count': len(missing_skills)
        }
    
    def rank_candidates(self, candidates: List[Dict], job_skills: List[str]) -> List[Dict]:
        """
        Rank candidates based on their match with job requirements
        candidates: List of dicts with 'id', 'name', 'skills'
        Returns sorted list with match scores
        """
        ranked = []
        
        for candidate in candidates:
            match_info = self.calculate_match_detailed(
                candidate.get('skills', []),
                job_skills
            )
            
            ranked.append({
                'id': candidate.get('id'),
                'name': candidate.get('name'),
                'match_score': match_info['match_score'],
                'exact_match_percentage': match_info['exact_match_percentage'],
                'matched_skills': match_info['matched_skills'],
                'missing_skills': match_info['missing_skills'],
                'matched_count': match_info['matched_count']
            })
        
        # Sort by match score (descending)
        ranked.sort(key=lambda x: x['match_score'], reverse=True)
        
        return ranked
    
    def rank_jobs(self, jobs: List[Dict], student_skills: List[str]) -> List[Dict]:
        """
        Rank jobs for a student based on skill match
        jobs: List of dicts with 'id', 'title', 'skills_required'
        Returns sorted list with match scores
        """
        ranked = []
        
        for job in jobs:
            match_info = self.calculate_match_detailed(
                student_skills,
                job.get('skills_required', [])
            )
            
            ranked.append({
                'id': job.get('id'),
                'title': job.get('title'),
                'company': job.get('company', ''),
                'match_score': match_info['match_score'],
                'exact_match_percentage': match_info['exact_match_percentage'],
                'matched_skills': match_info['matched_skills'],
                'missing_skills': match_info['missing_skills'],
                'matched_count': match_info['matched_count']
            })
        
        # Sort by match score (descending)
        ranked.sort(key=lambda x: x['match_score'], reverse=True)
        
        return ranked


# Example usage
if __name__ == "__main__":
    matcher = SkillMatcher()
    
    # Example student skills
    student_skills = ['python', 'django', 'rest api', 'sql', 'git', 'docker']
    
    # Example job requirements
    job_skills = ['python', 'django', 'postgresql', 'rest api', 'docker', 'aws']
    
    # Calculate match
    result = matcher.calculate_match_detailed(student_skills, job_skills)
    
    print(f"Match Score: {result['match_score']}%")
    print(f"Exact Match: {result['exact_match_percentage']}%")
    print(f"Matched Skills: {result['matched_skills']}")
    print(f"Missing Skills: {result['missing_skills']}")
