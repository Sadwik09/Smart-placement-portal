"""
Resume Parser Module
Extracts text and skills from PDF resumes
"""

import PyPDF2
import pdfplumber
import re
import spacy
from typing import List, Dict


class ResumeParser:
    """Parse PDF resumes and extract skills"""
    
    def __init__(self):
        """Initialize with spaCy model"""
        try:
            self.nlp = spacy.load('en_core_web_sm')
        except OSError:
            print("Please download spaCy model: python -m spacy download en_core_web_sm")
            self.nlp = None
    
    def extract_text_pypdf2(self, pdf_path: str) -> str:
        """Extract text using PyPDF2"""
        text = ""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
        except Exception as e:
            print(f"Error extracting text with PyPDF2: {e}")
        return text
    
    def extract_text_pdfplumber(self, pdf_path: str) -> str:
        """Extract text using pdfplumber (more accurate)"""
        text = ""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text
        except Exception as e:
            print(f"Error extracting text with pdfplumber: {e}")
        return text
    
    def extract_text(self, pdf_path: str) -> str:
        """Extract text from PDF (tries both methods)"""
        text = self.extract_text_pdfplumber(pdf_path)
        if not text:
            text = self.extract_text_pypdf2(pdf_path)
        return text
    
    def clean_text(self, text: str) -> str:
        """Clean extracted text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep alphanumeric and common punctuation
        text = re.sub(r'[^a-zA-Z0-9\s\.,\-\+\#]', '', text)
        return text.strip()
    
    def extract_skills_regex(self, text: str) -> List[str]:
        """Extract skills using regex patterns"""
        # Common technical skills
        skills_keywords = [
            'python', 'java', 'javascript', 'c\\+\\+', 'c#', 'react', 'angular', 'vue',
            'node', 'django', 'flask', 'spring', 'sql', 'nosql', 'mongodb', 'postgresql',
            'mysql', 'html', 'css', 'typescript', 'php', 'ruby', 'go', 'rust', 'kotlin',
            'swift', 'machine learning', 'deep learning', 'ai', 'data science', 'nlp',
            'computer vision', 'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy',
            'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'devops', 'ci/cd', 'git',
            'restful api', 'graphql', 'microservices', 'agile', 'scrum', 'rest api'
        ]
        
        text_lower = text.lower()
        found_skills = []
        
        for skill in skills_keywords:
            pattern = r'\b' + skill + r'\b'
            if re.search(pattern, text_lower):
                # Normalize skill name
                skill_name = skill.replace('\\', '')
                if skill_name not in found_skills:
                    found_skills.append(skill_name)
        
        return found_skills
    
    def extract_skills_nlp(self, text: str) -> List[str]:
        """Extract skills using NLP (Named Entity Recognition)"""
        if not self.nlp:
            return []
        
        doc = self.nlp(text)
        skills = []
        
        # Extract organizations and products (often represent technologies)
        for ent in doc.ents:
            if ent.label_ in ['ORG', 'PRODUCT']:
                skills.append(ent.text.lower())
        
        return list(set(skills))
    
    def extract_skills(self, pdf_path: str) -> Dict:
        """Extract all skills from resume"""
        # Extract and clean text
        text = self.extract_text(pdf_path)
        cleaned_text = self.clean_text(text)
        
        # Extract skills using both methods
        regex_skills = self.extract_skills_regex(cleaned_text)
        nlp_skills = self.extract_skills_nlp(cleaned_text)
        
        # Combine and deduplicate
        all_skills = list(set(regex_skills + nlp_skills))
        
        return {
            'raw_text': text,
            'cleaned_text': cleaned_text,
            'skills': all_skills,
            'skill_count': len(all_skills)
        }
    
    def extract_email(self, text: str) -> str:
        """Extract email from text"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        match = re.search(email_pattern, text)
        return match.group(0) if match else None
    
    def extract_phone(self, text: str) -> str:
        """Extract phone number from text"""
        phone_pattern = r'\b\d{10}\b|\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b'
        match = re.search(phone_pattern, text)
        return match.group(0) if match else None


# Example usage
if __name__ == "__main__":
    parser = ResumeParser()
    
    # Test with a sample PDF
    result = parser.extract_skills('sample_resume.pdf')
    print(f"Found {result['skill_count']} skills:")
    print(result['skills'])
