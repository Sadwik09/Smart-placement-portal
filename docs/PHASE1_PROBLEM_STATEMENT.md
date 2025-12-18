# Phase 1: Problem Statement & Requirement Analysis

## 📋 Problem Statement

### Current Challenges in Campus Placements:

1. **Manual Process**: Placement officers manually match student profiles with job requirements
2. **Time-Consuming**: Reviewing hundreds of resumes for each job posting
3. **Inefficient Matching**: Students apply to irrelevant jobs; recruiters miss suitable candidates
4. **Lack of Insights**: No data-driven approach to track placement trends
5. **Communication Gaps**: Delayed notifications and scattered information

### Proposed Solution:

**Smart Placement Portal** - An AI-powered system that automates campus placement management through:
- Intelligent resume parsing and skill extraction
- Automated skill matching between students and jobs
- AI-based recommendations for both students and recruiters
- Centralized dashboard for placement tracking and analytics

---

## 🎯 Project Objectives

### Primary Objectives:
1. ✅ Automate the placement process to reduce manual effort
2. ✅ Implement AI-based skill matching for accurate job-student pairing
3. ✅ Provide personalized job recommendations to students
4. ✅ Help recruiters find the best-fit candidates efficiently
5. ✅ Create a centralized platform for all placement activities

### Secondary Objectives:
1. 📊 Generate placement analytics and insights
2. 📈 Identify skill gaps in students
3. 📧 Automate notifications and communication
4. 📅 Streamline interview scheduling
5. 🔒 Ensure secure and role-based access

---

## 🎓 Target Users

### 1. **Students**
- **Need**: Find relevant job opportunities matching their skills
- **Benefits**: 
  - Personalized job recommendations
  - Automated skill analysis
  - Easy application tracking
  - Interview scheduling

### 2. **Recruiters**
- **Need**: Identify qualified candidates efficiently
- **Benefits**:
  - AI-ranked candidate lists
  - Skill-based filtering
  - Resume database access
  - Application management

### 3. **Admin (TPO - Training & Placement Officer)**
- **Need**: Manage the entire placement process
- **Benefits**:
  - User approval and management
  - Placement analytics dashboard
  - System monitoring
  - Report generation

---

## 🔧 Scope of the Project

### In-Scope (MVP):

#### Core Features:
1. **User Management**
   - Registration & Login (JWT authentication)
   - Role-based access control
   - Profile management

2. **Resume Management**
   - Resume upload (PDF)
   - Automated parsing and skill extraction
   - Resume database

3. **Job Management**
   - Job posting by recruiters
   - Job listings for students
   - Application system

4. **AI/ML Features**
   - Skill matching algorithm (TF-IDF + Cosine Similarity)
   - Job recommendations for students
   - Candidate recommendations for recruiters
   - Resume scoring

5. **Admin Dashboard**
   - User approval
   - Placement statistics
   - System management

### Extended Features (Phase 2):
- Interview scheduling system
- Email notifications
- Skill gap analysis
- Advanced analytics (branch-wise, year-wise)
- Document generation (offer letters, reports)

### Out-of-Scope:
- Video interview platform
- Payment processing
- Mobile application (web-responsive only)
- Third-party job board integration

---

## 📋 Feature List (Detailed)

### 🔐 Authentication & Authorization
| Feature | User | Description | Priority |
|---------|------|-------------|----------|
| Registration | All | Email-based signup with role selection | High |
| Login | All | JWT token-based authentication | High |
| Role-based Access | All | Different dashboards for Student/Recruiter/Admin | High |
| Password Reset | All | Email-based password recovery | Medium |
| Profile Management | All | Update personal information | High |

### 👨‍🎓 Student Features
| Feature | Description | Priority |
|---------|-------------|----------|
| Resume Upload | Upload PDF resume | High |
| Profile Creation | Skills, education, CGPA, projects | High |
| Job Search | Browse available jobs | High |
| Job Application | Apply to jobs with one click | High |
| View Recommendations | AI-suggested jobs based on profile | High |
| Application Tracking | Track application status | Medium |
| Skill Gap Analysis | Identify missing skills | Low |

### 🏢 Recruiter Features
| Feature | Description | Priority |
|---------|-------------|----------|
| Company Profile | Company details, industry | High |
| Job Posting | Create job with requirements | High |
| View Applications | List of students who applied | High |
| Candidate Recommendations | AI-ranked student list | High |
| Resume Database | Search student resumes | Medium |
| Shortlist Candidates | Shortlist for interview | Medium |
| Schedule Interviews | Set interview date/time | Low |

### 👤 Admin Features
| Feature | Description | Priority |
|---------|-------------|----------|
| User Approval | Approve/reject registrations | High |
| User Management | View, edit, delete users | High |
| Job Management | Approve/remove job postings | Medium |
| Analytics Dashboard | Placement statistics | Medium |
| Generate Reports | Excel/PDF reports | Low |
| System Logs | Activity monitoring | Low |

### 🤖 AI/ML Features
| Feature | Description | Priority |
|---------|-------------|----------|
| Resume Parsing | Extract text and skills from PDF | High |
| Skill Extraction | NLP-based keyword extraction | High |
| Skill Matching | TF-IDF + Cosine Similarity | High |
| Job Recommendations | Rank jobs for each student | High |
| Candidate Ranking | Rank students for each job | High |
| Resume Scoring | Score resume quality (0-100) | Medium |

---

## 📊 Success Metrics

1. **Efficiency**: Reduce placement process time by 60%
2. **Accuracy**: 80%+ matching accuracy between skills and jobs
3. **User Adoption**: 90%+ of students and recruiters use the platform
4. **Satisfaction**: 4/5+ average user rating

---

## 🚀 Project Timeline

**Total Duration**: 13 weeks

- **Weeks 1-2**: Planning & Design
- **Weeks 3-6**: Core Development (Auth, Resume, Jobs)
- **Weeks 7-8**: AI/ML Implementation
- **Weeks 9-10**: Extended Features
- **Weeks 11-12**: Testing & Deployment
- **Week 13**: Documentation & Viva Preparation

---

**Document Version**: 1.0  
**Last Updated**: December 17, 2025  
**Status**: Approved ✅
