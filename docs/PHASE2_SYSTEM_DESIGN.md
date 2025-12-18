# Phase 2: System Design & Architecture

## 🏛️ System Architecture

### Architecture Type: **3-Tier Client-Server Architecture**

```
┌─────────────────────────────────────────────────────────┐
│                    PRESENTATION TIER                     │
│                    (React Frontend)                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Student    │  │  Recruiter   │  │    Admin     │ │
│  │  Dashboard   │  │  Dashboard   │  │  Dashboard   │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
│            Role-based UI Components                     │
└────────────────────┬────────────────────────────────────┘
                     │ REST API (JSON)
                     │ JWT Authentication
┌────────────────────▼────────────────────────────────────┐
│                   APPLICATION TIER                       │
│                (Django REST Framework)                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │     Auth     │  │     Jobs     │  │   Resumes    │ │
│  │   Service    │  │   Service    │  │   Service    │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │     ML       │  │  Analytics   │  │    Email     │ │
│  │ Integration  │  │   Service    │  │   Service    │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
┌───────▼──────┐ ┌──▼─────────┐ ┌▼──────────────┐
│     DATA     │ │   ML       │ │   FILE        │
│    TIER      │ │  MODELS    │ │  STORAGE      │
│              │ │            │ │               │
│  PostgreSQL  │ │ .pkl files │ │   Uploads/    │
└──────────────┘ └────────────┘ └───────────────┘
```

### Communication Flow:
1. **Frontend → Backend**: REST API calls with JWT tokens
2. **Backend → Database**: ORM queries (Django ORM)
3. **Backend → ML Module**: Python function calls for predictions
4. **Backend → File System**: Resume storage and retrieval

---

## 🗄️ Database Design (ER Diagram)

### Entity Relationship Diagram

```
┌─────────────────┐
│      User       │
├─────────────────┤
│ PK id           │
│    email        │──────┐
│    password     │      │
│    role         │      │ 1:1
│    is_approved  │      │
│    created_at   │      │
└─────────────────┘      │
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         │ 1:1           │               │ 1:1
┌────────▼─────────┐     │      ┌────────▼─────────┐
│     Student      │     │      │    Recruiter     │
├──────────────────┤     │      ├──────────────────┤
│ PK id            │     │      │ PK id            │
│ FK user_id       │     │      │ FK user_id       │
│    name          │     │      │    company_name  │
│    roll_number   │     │      │    company_desc  │
│    branch        │     │      │    industry      │
│    cgpa          │     │      │    website       │
│    phone         │     │      │    phone         │
│    skills        │     │      │    location      │
│    year          │     │      └──────────────────┘
└────────┬─────────┘     │              │
         │ 1:M           │              │ 1:M
         │               │              │
┌────────▼─────────┐     │      ┌───────▼──────────┐
│     Resume       │     │      │       Job        │
├──────────────────┤     │      ├──────────────────┤
│ PK id            │     │      │ PK id            │
│ FK student_id    │     │      │ FK recruiter_id  │
│    file_path     │     │      │    title         │
│    parsed_text   │     │      │    description   │
│    skills_json   │     │      │    skills_req    │
│    score         │     │      │    experience    │
│    uploaded_at   │     │      │    ctc           │
└──────────────────┘     │      │    location      │
                         │      │    type          │
                         │      │    deadline      │
                         │      │    is_active     │
                         │      └──────────────────┘
                         │              │
                         │              │ M:N
                         │      ┌───────▼──────────┐
                         │      │   Application    │
                         │      ├──────────────────┤
                         │      │ PK id            │
                         │      │ FK student_id    │────┐
                         │      │ FK job_id        │    │
                         │      │    match_score   │    │
                         │      │    status        │    │
                         │      │    applied_at    │    │
                         │      └──────────────────┘    │
                         │                              │
                 1:1     │                              │
         ┌───────────────┘                              │
         │                                              │
┌────────▼─────────┐                    ┌───────────────▼──────────┐
│      Admin       │                    │      Interview           │
├──────────────────┤                    ├──────────────────────────┤
│ PK id            │                    │ PK id                    │
│ FK user_id       │                    │ FK application_id        │
│    name          │                    │    scheduled_date        │
│    phone         │                    │    scheduled_time        │
└──────────────────┘                    │    mode (online/offline) │
                                        │    status                │
                                        │    feedback              │
                                        └──────────────────────────┘
```

### Database Schema Details

#### Table: `users`
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('student', 'recruiter', 'admin')),
    is_approved BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Table: `students`
```sql
CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    roll_number VARCHAR(50) UNIQUE NOT NULL,
    branch VARCHAR(100),
    year INTEGER,
    cgpa DECIMAL(3,2),
    phone VARCHAR(15),
    skills TEXT[], -- Array of skills
    linkedin VARCHAR(255),
    github VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Table: `recruiters`
```sql
CREATE TABLE recruiters (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    company_name VARCHAR(255) NOT NULL,
    company_description TEXT,
    industry VARCHAR(100),
    website VARCHAR(255),
    phone VARCHAR(15),
    location VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Table: `admins`
```sql
CREATE TABLE admins (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(15),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Table: `resumes`
```sql
CREATE TABLE resumes (
    id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students(id) ON DELETE CASCADE,
    file_path VARCHAR(500) NOT NULL,
    parsed_text TEXT,
    skills_json JSONB, -- Extracted skills
    score DECIMAL(5,2), -- Resume score 0-100
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Table: `jobs`
```sql
CREATE TABLE jobs (
    id SERIAL PRIMARY KEY,
    recruiter_id INTEGER REFERENCES recruiters(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    skills_required TEXT[], -- Array of skills
    experience_required VARCHAR(50),
    ctc VARCHAR(50),
    location VARCHAR(255),
    job_type VARCHAR(50), -- Full-time, Internship
    deadline DATE,
    is_active BOOLEAN DEFAULT TRUE,
    posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Table: `applications`
```sql
CREATE TABLE applications (
    id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students(id) ON DELETE CASCADE,
    job_id INTEGER REFERENCES jobs(id) ON DELETE CASCADE,
    match_score DECIMAL(5,2), -- AI match score
    status VARCHAR(50) DEFAULT 'applied', -- applied, shortlisted, rejected, selected
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(student_id, job_id) -- Prevent duplicate applications
);
```

#### Table: `interviews`
```sql
CREATE TABLE interviews (
    id SERIAL PRIMARY KEY,
    application_id INTEGER REFERENCES applications(id) ON DELETE CASCADE,
    scheduled_date DATE,
    scheduled_time TIME,
    mode VARCHAR(20), -- online, offline
    location TEXT,
    status VARCHAR(50) DEFAULT 'scheduled',
    feedback TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 📊 UML Diagrams

### 1. Use Case Diagram

```
                    Smart Placement Portal
    ┌────────────────────────────────────────────────┐
    │                                                │
    │    ┌──────────────────┐                       │
    │    │  Register/Login  │                       │
    │    └────────┬─────────┘                       │
    │             │                                  │
    │    ┌────────┼────────────────────┐            │
    │    │        │                    │            │
Student  │   Recruiter              Admin           │
    │    │        │                    │            │
    │  ┌─▼────────▼─┐          ┌───────▼───────┐   │
    │  │ View Jobs  │          │ Approve Users │   │
    │  └────────────┘          └───────────────┘   │
    │  ┌────────────┐          ┌───────────────┐   │
    │  │ Apply Job  │          │  View Stats   │   │
    │  └────────────┘          └───────────────┘   │
    │  ┌────────────┐          ┌───────────────┐   │
    │  │Upload Resume│         │ Manage Jobs   │   │
    │  └────────────┘          └───────────────┘   │
    │  ┌────────────┐                              │
    │  │Get Recom.  │          ┌───────────────┐   │
    │  └────────────┘          │  Post Job     │   │
    │                          └───────────────┘   │
    │                          ┌───────────────┐   │
    │                          │View Applicants│   │
    │                          └───────────────┘   │
    │                          ┌───────────────┐   │
    │                          │Get Candidates │   │
    │                          └───────────────┘   │
    └────────────────────────────────────────────────┘
```

### 2. Sequence Diagram: Job Application with AI Matching

```
Student    Frontend    Backend      ML Module    Database
  │           │           │              │            │
  │─Browse───>│           │              │            │
  │           │─Get Jobs─>│              │            │
  │           │           │──Query Jobs─>│            │
  │           │           │<─Job List────│            │
  │           │<─Display──│              │            │
  │─Click────>│           │              │            │
  │ Apply     │           │              │            │
  │           │─Apply────>│              │            │
  │           │ Request   │──Get Student─>│            │
  │           │           │<─Profile─────│            │
  │           │           │──Get Job────>│            │
  │           │           │<─Details─────│            │
  │           │           │              │            │
  │           │           │─Calculate───>│            │
  │           │           │ Match Score  │            │
  │           │           │<─Score: 87%──│            │
  │           │           │              │            │
  │           │           │─Save App────>│            │
  │           │           │ (score=87)   │            │
  │           │           │<─Success─────│            │
  │           │<─Applied──│              │            │
  │<─Success──│           │              │            │
  │ Message   │           │              │            │
```

### 3. Activity Diagram: Resume Upload & Parsing

```
      START
        │
        ▼
   Upload Resume
        │
        ▼
   Validate File
   (PDF?, Size?)
        │
    ┌───┴───┐
    │  No   │──> Error: Invalid File
    │       │
    └───┬───┘
        │ Yes
        ▼
  Save to Server
        │
        ▼
   Extract Text
   (PyPDF2/pdfplumber)
        │
        ▼
  Clean Text Data
        │
        ▼
   Extract Skills
   (NLP/Regex)
        │
        ▼
  Calculate Score
        │
        ▼
   Save to Database
        │
        ▼
   Return Success
        │
        ▼
       END
```

---

## 🔄 API Design (REST Endpoints)

### Authentication APIs
```
POST   /api/auth/register          - User registration
POST   /api/auth/login             - User login (returns JWT)
POST   /api/auth/logout            - User logout
POST   /api/auth/refresh-token     - Refresh JWT token
POST   /api/auth/forgot-password   - Password reset request
```

### Student APIs
```
GET    /api/students/profile       - Get student profile
PUT    /api/students/profile       - Update profile
POST   /api/students/resume        - Upload resume
GET    /api/students/resume        - Get resume details
GET    /api/students/jobs          - Browse jobs
GET    /api/students/recommendations - Get job recommendations
POST   /api/students/apply/:jobId  - Apply to job
GET    /api/students/applications  - Get application history
```

### Recruiter APIs
```
GET    /api/recruiters/profile     - Get recruiter profile
PUT    /api/recruiters/profile     - Update profile
POST   /api/jobs                   - Create job posting
GET    /api/jobs                   - Get all jobs
GET    /api/jobs/:id               - Get job details
PUT    /api/jobs/:id               - Update job
DELETE /api/jobs/:id               - Delete job
GET    /api/jobs/:id/applicants    - Get applicants for job
GET    /api/recruiters/recommendations - Get candidate recommendations
```

### Admin APIs
```
GET    /api/admin/users            - Get all users
PUT    /api/admin/users/:id/approve - Approve user
DELETE /api/admin/users/:id        - Delete user
GET    /api/admin/analytics        - Get placement stats
GET    /api/admin/reports          - Generate reports
```

### ML APIs (Internal)
```
POST   /api/ml/parse-resume        - Parse resume
POST   /api/ml/match-score         - Calculate match score
POST   /api/ml/recommend-jobs      - Get job recommendations
POST   /api/ml/recommend-candidates - Get candidate recommendations
POST   /api/ml/score-resume        - Score resume quality
```

---

## 🧠 Machine Learning Architecture

### ML Pipeline

```
Input (Resume PDF)
       │
       ▼
┌──────────────────┐
│  Text Extraction │ → PyPDF2/pdfplumber
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Preprocessing   │ → Lowercase, remove special chars
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Skill Extraction │ → Regex + NLP (spaCy)
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Vectorization   │ → TF-IDF Vectorizer
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Cosine Similarity│ → Match student skills vs job skills
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Match Score %   │ → 0-100%
└──────────────────┘
```

### Algorithms Used:
1. **TF-IDF (Term Frequency-Inverse Document Frequency)**: Convert text to numerical vectors
2. **Cosine Similarity**: Measure similarity between skill vectors
3. **Content-Based Filtering**: Recommendation based on profile matching

---

## 🔒 Security Architecture

1. **Authentication**: JWT tokens (access + refresh)
2. **Authorization**: Role-based access control (RBAC)
3. **Password Storage**: bcrypt hashing
4. **Data Validation**: Input sanitization
5. **CORS**: Configured for frontend domain
6. **SQL Injection Prevention**: ORM usage
7. **File Upload Security**: File type validation, size limits

---

**Document Version**: 1.0  
**Last Updated**: December 17, 2025  
**Status**: Approved ✅
