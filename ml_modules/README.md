# Machine Learning Modules for Smart Placement Portal

## Overview

This directory contains all ML-related modules for:
- Resume parsing and text extraction
- Skill extraction using NLP
- Skill matching algorithm (TF-IDF + Cosine Similarity)
- Job recommendation system
- Resume scoring

## Setup

### 1. Install Dependencies

```bash
cd ml_modules
pip install -r requirements.txt
```

### 2. Download NLP Models

```bash
python -m spacy download en_core_web_sm
python -m nltk.downloader punkt stopwords
```

## Modules

### 1. Resume Parser (`resume_parser/`)
- Extract text from PDF resumes
- Clean and preprocess text
- Extract skills using regex and NLP

### 2. Skill Matcher (`skill_matcher/`)
- TF-IDF vectorization
- Cosine similarity calculation
- Match score generation

### 3. Recommender (`recommender/`)
- Job recommendations for students
- Candidate recommendations for recruiters
- Ranking algorithms

### 4. Resume Scorer (`resume_scorer/`)
- Score resume quality (0-100)
- Check keyword relevance
- Format analysis

## Usage

```python
from resume_parser import ResumeParser
from skill_matcher import SkillMatcher

# Parse resume
parser = ResumeParser()
skills = parser.extract_skills('path/to/resume.pdf')

# Match skills
matcher = SkillMatcher()
score = matcher.calculate_match(student_skills, job_skills)
```

## Technologies

- **PyPDF2/pdfplumber**: PDF text extraction
- **spaCy**: NLP processing
- **scikit-learn**: TF-IDF, cosine similarity
- **NLTK**: Text preprocessing
- **pandas**: Data manipulation
