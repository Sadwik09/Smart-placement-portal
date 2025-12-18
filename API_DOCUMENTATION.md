# 📚 Smart Placement Portal - Complete API Documentation

## Base URL
```
Development: http://localhost:8000/api
Production: https://your-domain.com/api
```

## Authentication
All protected endpoints require JWT authentication via Bearer token in the Authorization header:
```
Authorization: Bearer <access_token>
```

---

## 🔐 Authentication Endpoints

### Register User
```http
POST /auth/register/
```
**Body:**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "password2": "password123",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "1234567890",
  "role": "student"  // student | recruiter
}
```

### Login
```http
POST /auth/login/
```
**Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```
**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJ...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJ...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "student"
  }
}
```

### Refresh Token
```http
POST /auth/token/refresh/
```
**Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJ..."
}
```

---

## 👤 Student Profile Endpoints

### Get/Create Profile
```http
GET /students/profile/
POST /students/profile/
```
**POST Body:**
```json
{
  "roll_number": "CS2021001",
  "branch": "CSE",
  "year": 4,
  "cgpa": 8.5,
  "skills": ["Python", "Django", "React"],
  "bio": "Passionate developer...",
  "linkedin": "https://linkedin.com/in/johndoe",
  "github": "https://github.com/johndoe",
  "portfolio": "https://johndoe.dev"
}
```

### Update Profile
```http
PUT /students/profile/
```

### List All Students (with filters)
```http
GET /students/list/?branch=CSE&year=4&min_cgpa=7.0&search=john
```

---

## 💼 Job Endpoints

### List Jobs (with filters)
```http
GET /jobs/?search=software&job_type=full_time&location=Bangalore&skills=Python
```

### Get Job Details
```http
GET /jobs/{job_id}/
```

### Create Job (Recruiter only)
```http
POST /jobs/
```
**Body:**
```json
{
  "title": "Software Engineer",
  "description": "We are looking for...",
  "job_type": "full_time",
  "company_name": "Tech Corp",
  "location": "Bangalore",
  "is_remote": false,
  "ctc": "8-10 LPA",
  "experience_required": "0-2 years",
  "education_required": "B.Tech/B.E.",
  "skills_required": ["Python", "Django", "PostgreSQL"],
  "min_cgpa": 7.0,
  "deadline": "2025-12-31"
}
```

### Apply to Job (Student only)
```http
POST /jobs/{job_id}/apply/
```
**Body:**
```json
{
  "cover_letter": "I am interested in this position because..."
}
```

### My Applications
```http
GET /jobs/applications/my/
```

---

## 📄 Resume Endpoints

### Upload Resume
```http
POST /resumes/upload/
```
**Body:** multipart/form-data with `file` field (PDF only, max 5MB)

**Response:**
```json
{
  "message": "Resume uploaded and parsed successfully",
  "resume": {...},
  "parsing_results": {
    "skills": ["Python", "Django", "React"],
    "contact_info": {
      "email": "john@example.com",
      "phone": "1234567890"
    },
    "score": 85,
    "score_breakdown": {
      "skills_score": 90,
      "experience_score": 80,
      "education_score": 85,
      "formatting_score": 85,
      "keywords_score": 80,
      "length_score": 90,
      "contact_info_score": 100
    },
    "recommendations": [
      "Add more quantifiable achievements",
      "Include LinkedIn profile"
    ]
  }
}
```

### List Resumes
```http
GET /resumes/
```

### Download Resume
```http
GET /resumes/{resume_id}/download/
```

---

## 🤖 ML Integration Endpoints

### Get Job Recommendations (Student)
```http
GET /ml/job-recommendations/
```
**Response:**
```json
{
  "student_skills": ["Python", "Django", "React"],
  "total_jobs": 15,
  "recommendations": [
    {
      "id": 1,
      "title": "Backend Developer",
      "company_name": "Tech Corp",
      "location": "Bangalore",
      "ctc": "10-12 LPA",
      "match_score": 85.5,
      "matched_skills": ["Python", "Django"],
      "missing_skills": ["PostgreSQL"],
      "deadline": "2025-12-31"
    }
  ]
}
```

### Get Candidate Recommendations (Recruiter)
```http
GET /ml/candidate-recommendations/{job_id}/
```

### Calculate Match Score
```http
POST /ml/calculate-match/
```
**Body:**
```json
{
  "job_id": 1,
  "student_id": 1
}
```

### Get Resume Score
```http
GET /ml/resume-score/
GET /ml/resume-score/{resume_id}/
```

---

## 📅 Interview Endpoints

### Schedule Interview (Recruiter)
```http
POST /jobs/interviews/schedule/
```
**Body:**
```json
{
  "application_id": 1,
  "scheduled_date": "2025-12-20",
  "scheduled_time": "14:00:00",
  "mode": "online",
  "meeting_link": "https://meet.google.com/abc-defg-hij",
  "interviewer_name": "Jane Smith",
  "interviewer_email": "jane@company.com",
  "notes": "Technical round - DSA focus"
}
```

### My Interviews (Student)
```http
GET /jobs/interviews/my/
```

### Interview Details
```http
GET /jobs/interviews/{interview_id}/
PUT /jobs/interviews/{interview_id}/  // Update (Recruiter only)
```

---

## 📊 Analytics Endpoints (Admin)

### Dashboard Stats
```http
GET /analytics/dashboard/
```
**Response:**
```json
{
  "total_users": 150,
  "total_students": 100,
  "total_recruiters": 50,
  "total_jobs": 75,
  "active_jobs": 60,
  "total_applications": 500,
  "pending_approvals": 5
}
```

### User Approvals
```http
GET /analytics/approvals/  // List pending users
POST /analytics/approvals/{user_id}/approve/  // Approve/Reject user
```
**POST Body:**
```json
{
  "approved": true
}
```

### Placement Statistics
```http
GET /analytics/statistics/
```

---

## 🔑 Status Codes

- `200 OK` - Success
- `201 Created` - Resource created
- `400 Bad Request` - Invalid data
- `401 Unauthorized` - Not authenticated
- `403 Forbidden` - Not authorized
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

---

## 📝 Data Models

### Job Status
- `applied` - Application submitted
- `reviewing` - Under review
- `shortlisted` - Shortlisted for interview
- `interview_scheduled` - Interview scheduled
- `selected` - Selected for job
- `rejected` - Application rejected

### Interview Mode
- `online` - Online interview
- `offline` - In-person interview
- `phone` - Phone interview

### Job Types
- `full_time` - Full-time position
- `internship` - Internship
- `part_time` - Part-time position
- `contract` - Contract position

---

## 🧪 Testing with cURL

```bash
# Register
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123","password2":"test123","first_name":"Test","last_name":"User","phone":"1234567890","role":"student"}'

# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'

# Get Jobs (with auth)
curl -X GET http://localhost:8000/api/jobs/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

**📖 For more details, visit the project repository or contact the development team.**
