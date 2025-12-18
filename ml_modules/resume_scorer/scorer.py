"""
Resume Scorer Module
Scores resume quality on a scale of 0-100
"""

import re
from typing import Dict, List


class ResumeScorer:
    """Score resume quality based on various factors"""
    
    def __init__(self):
        """Initialize scorer with weights"""
        self.weights = {
            'skills': 0.30,
            'experience': 0.25,
            'education': 0.15,
            'formatting': 0.10,
            'keywords': 0.10,
            'length': 0.05,
            'contact_info': 0.05,
        }
    
    def score_resume(self, resume_data: Dict) -> Dict:
        """
        Score resume based on multiple factors
        
        Args:
            resume_data: Dict with 'text', 'skills', etc.
        
        Returns:
            Dict with overall score and breakdown
        """
        text = resume_data.get('text', '')
        skills = resume_data.get('skills', [])
        
        scores = {
            'skills_score': self._score_skills(skills),
            'experience_score': self._score_experience(text),
            'education_score': self._score_education(text),
            'formatting_score': self._score_formatting(text),
            'keywords_score': self._score_keywords(text),
            'length_score': self._score_length(text),
            'contact_score': self._score_contact_info(text),
        }
        
        # Calculate weighted overall score
        overall_score = (
            scores['skills_score'] * self.weights['skills'] +
            scores['experience_score'] * self.weights['experience'] +
            scores['education_score'] * self.weights['education'] +
            scores['formatting_score'] * self.weights['formatting'] +
            scores['keywords_score'] * self.weights['keywords'] +
            scores['length_score'] * self.weights['length'] +
            scores['contact_score'] * self.weights['contact_info']
        )
        
        return {
            'overall_score': round(overall_score, 2),
            'breakdown': scores,
            'recommendations': self._generate_recommendations(scores)
        }
    
    def _score_skills(self, skills: List[str]) -> float:
        """Score based on number of skills listed"""
        skill_count = len(skills)
        
        if skill_count >= 10:
            return 100
        elif skill_count >= 7:
            return 85
        elif skill_count >= 5:
            return 70
        elif skill_count >= 3:
            return 50
        else:
            return 30
    
    def _score_experience(self, text: str) -> float:
        """Score based on experience keywords and structure"""
        score = 0
        text_lower = text.lower()
        
        experience_keywords = [
            'experience', 'worked', 'developed', 'managed', 'led',
            'implemented', 'designed', 'created', 'built', 'achieved',
            'project', 'internship', 'responsibility', 'role'
        ]
        
        # Count experience keywords
        keyword_count = sum(1 for keyword in experience_keywords if keyword in text_lower)
        score += min(keyword_count * 5, 50)
        
        # Check for years of experience
        if re.search(r'\d+\s*(year|yr)', text_lower):
            score += 20
        
        # Check for bullet points (good formatting)
        if '•' in text or '●' in text or re.search(r'^\s*[-*]', text, re.MULTILINE):
            score += 15
        
        # Check for numbers/metrics (quantifiable achievements)
        if re.search(r'\d+%|\d+\+|increased|improved|reduced', text_lower):
            score += 15
        
        return min(score, 100)
    
    def _score_education(self, text: str) -> float:
        """Score based on education information"""
        score = 0
        text_lower = text.lower()
        
        education_keywords = [
            'education', 'university', 'college', 'institute',
            'bachelor', 'master', 'phd', 'degree', 'diploma',
            'b.tech', 'm.tech', 'b.sc', 'm.sc', 'mba', 'bba'
        ]
        
        # Check for education section
        if any(keyword in text_lower for keyword in education_keywords):
            score += 40
        
        # Check for GPA/CGPA
        if re.search(r'(gpa|cgpa)\s*:?\s*\d+\.?\d*', text_lower):
            score += 30
        
        # Check for graduation year
        if re.search(r'(graduated|graduation|passout)\s*:?\s*(20\d{2})', text_lower):
            score += 15
        
        # Check for major/specialization
        if re.search(r'(major|specialization|stream|branch)\s*:?', text_lower):
            score += 15
        
        return min(score, 100)
    
    def _score_formatting(self, text: str) -> float:
        """Score based on resume formatting and structure"""
        score = 0
        
        # Check for proper sections
        sections = ['education', 'experience', 'skills', 'projects']
        sections_found = sum(1 for section in sections if section in text.lower())
        score += sections_found * 20
        
        # Check for proper capitalization
        if any(word.istitle() for word in text.split()[:50]):
            score += 15
        
        # Check for consistent line breaks (not too many empty lines)
        empty_lines = text.count('\n\n')
        if 3 <= empty_lines <= 10:
            score += 5
        
        return min(score, 100)
    
    def _score_keywords(self, text: str) -> float:
        """Score based on professional keywords"""
        score = 0
        text_lower = text.lower()
        
        professional_keywords = [
            'leadership', 'team', 'collaboration', 'communication',
            'problem-solving', 'analytical', 'innovative', 'efficient',
            'responsible', 'organized', 'detail-oriented', 'proactive'
        ]
        
        keyword_count = sum(1 for keyword in professional_keywords if keyword in text_lower)
        score = min(keyword_count * 10, 100)
        
        return score
    
    def _score_length(self, text: str) -> float:
        """Score based on resume length (word count)"""
        word_count = len(text.split())
        
        # Ideal range: 300-800 words
        if 300 <= word_count <= 800:
            return 100
        elif 200 <= word_count < 300:
            return 80
        elif 800 < word_count <= 1000:
            return 80
        elif word_count < 200:
            return 50
        else:
            return 40
    
    def _score_contact_info(self, text: str) -> float:
        """Score based on contact information"""
        score = 0
        
        # Check for email
        if re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text):
            score += 35
        
        # Check for phone number
        if re.search(r'\b\d{10}\b|\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b', text):
            score += 30
        
        # Check for LinkedIn
        if 'linkedin' in text.lower():
            score += 20
        
        # Check for GitHub
        if 'github' in text.lower():
            score += 15
        
        return min(score, 100)
    
    def _generate_recommendations(self, scores: Dict) -> List[str]:
        """Generate improvement recommendations based on scores"""
        recommendations = []
        
        if scores['skills_score'] < 70:
            recommendations.append("Add more relevant technical skills to strengthen your profile.")
        
        if scores['experience_score'] < 60:
            recommendations.append("Include more details about your work experience and achievements.")
        
        if scores['education_score'] < 70:
            recommendations.append("Add comprehensive education details including GPA and relevant coursework.")
        
        if scores['formatting_score'] < 60:
            recommendations.append("Improve resume structure with clear sections (Education, Experience, Skills, Projects).")
        
        if scores['keywords_score'] < 50:
            recommendations.append("Include more professional keywords and soft skills.")
        
        if scores['length_score'] < 70:
            recommendations.append("Adjust resume length. Aim for 300-800 words for optimal readability.")
        
        if scores['contact_score'] < 80:
            recommendations.append("Ensure all contact information is included (email, phone, LinkedIn, GitHub).")
        
        if not recommendations:
            recommendations.append("Great resume! Keep it updated with recent achievements.")
        
        return recommendations


# Example usage
if __name__ == "__main__":
    scorer = ResumeScorer()
    
    sample_resume = {
        'text': """
        John Doe
        john.doe@email.com | 9876543210 | linkedin.com/in/johndoe
        
        EDUCATION
        B.Tech in Computer Science Engineering
        XYZ University, 2020-2024
        CGPA: 8.5/10
        
        EXPERIENCE
        Software Engineering Intern, ABC Company
        June 2023 - Aug 2023
        - Developed REST APIs using Django
        - Improved application performance by 30%
        
        SKILLS
        Python, Django, JavaScript, React, SQL, Git
        """,
        'skills': ['Python', 'Django', 'JavaScript', 'React', 'SQL', 'Git']
    }
    
    result = scorer.score_resume(sample_resume)
    print(f"Overall Score: {result['overall_score']}/100")
    print("\nBreakdown:")
    for category, score in result['breakdown'].items():
        print(f"  {category}: {score:.1f}")
    print("\nRecommendations:")
    for rec in result['recommendations']:
        print(f"  - {rec}")
