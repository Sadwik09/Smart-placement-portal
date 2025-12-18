# ✅ MongoDB Connected Successfully!

## Connection Details

**MongoDB URI:** `mongodb+srv://sadwik1409_db_user:SadwikSimply09@smart-placement-portal.pt0axg9.mongodb.net/`  
**Database Name:** `smart_placement_portal`  
**Status:** ✅ Connected and verified

---

## What's Been Configured

### ✅ Backend Setup
1. **Dependencies Installed:**
   - `pymongo>=4.0.0` - MongoDB Python driver
   - `dnspython>=2.0.0` - Required for MongoDB SRV connections

2. **Settings Updated:**
   - MongoDB connection configured in `settings.py`
   - Connection string stored in `MONGODB_URI`
   - Database name: `smart_placement_portal`
   - SQLite retained for Django admin/auth system

3. **MongoDB Utilities Created:**
   - **File:** `backend/placement_portal/mongodb_utils.py`
   - Helper class `MongoDB` for easy database operations
   - Collection constants in `Collections` class
   - CRUD operations: insert, find, update, delete
   - Automatic timestamp handling (created_at, updated_at)
   - Document serialization helpers

### ✅ Configuration Files Updated
- `requirements.txt` - Added pymongo and dnspython
- `.env.example` - Added MongoDB configuration section

---

## MongoDB Collections Structure

Your database will use these collections:

```python
Collections:
    USERS = 'users'                    # User accounts
    STUDENTS = 'students'              # Student profiles
    RECRUITERS = 'recruiters'          # Recruiter profiles
    JOBS = 'jobs'                      # Job postings
    APPLICATIONS = 'applications'      # Job applications
    RESUMES = 'resumes'                # Resume data
    INTERVIEWS = 'interviews'          # Interview schedules
    NOTIFICATIONS = 'notifications'    # User notifications
    ANALYTICS = 'analytics'            # Analytics data
```

---

## How to Use MongoDB in Your Code

### Example 1: Insert Data
```python
from placement_portal.mongodb_utils import MongoDB, Collections

# Insert a job posting
job_data = {
    'title': 'Software Engineer',
    'company': 'Tech Corp',
    'location': 'Mumbai',
    'salary': '10-15 LPA',
    'posted_by': 'recruiter_id'
}

job_id = MongoDB.insert_one(Collections.JOBS, job_data)
print(f'Job created with ID: {job_id}')
```

### Example 2: Find Data
```python
# Find all active jobs
jobs = MongoDB.find_many(
    Collections.JOBS,
    {'is_active': True}
)

# Find one specific job
job = MongoDB.find_one(
    Collections.JOBS,
    {'_id': job_id}
)
```

### Example 3: Update Data
```python
# Update job status
MongoDB.update_one(
    Collections.JOBS,
    {'_id': job_id},
    {'$set': {'is_active': False}}
)
```

### Example 4: Delete Data
```python
# Delete a job
MongoDB.delete_one(
    Collections.JOBS,
    {'_id': job_id}
)
```

### Example 5: Count Documents
```python
# Count total jobs
total_jobs = MongoDB.count_documents(Collections.JOBS)

# Count active jobs
active_jobs = MongoDB.count_documents(
    Collections.JOBS,
    {'is_active': True}
)
```

---

## Using MongoDB in Django Views

### Example View with MongoDB
```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from placement_portal.mongodb_utils import MongoDB, Collections, serialize_mongo_doc

class JobListView(APIView):
    def get(self, request):
        # Get all jobs from MongoDB
        jobs = MongoDB.find_many(Collections.JOBS)
        
        # Serialize MongoDB documents for JSON response
        serialized_jobs = [serialize_mongo_doc(job) for job in jobs]
        
        return Response({
            'jobs': serialized_jobs,
            'count': len(serialized_jobs)
        }, status=status.HTTP_200_OK)
    
    def post(self, request):
        # Create new job
        job_data = request.data
        job_id = MongoDB.insert_one(Collections.JOBS, job_data)
        
        return Response({
            'message': 'Job created successfully',
            'job_id': job_id
        }, status=status.HTTP_201_CREATED)
```

---

## MongoDB Indexes (For Performance)

Indexes are automatically created for:
- **users**: email (unique), username (unique)
- **jobs**: company_name, posted_by, is_active
- **applications**: job_id, student_id, status
- **notifications**: user_id, is_read

---

## Environment Variables

Add these to your `.env` file:

```env
# MongoDB Configuration
MONGODB_URI=mongodb+srv://sadwik1409_db_user:SadwikSimply09@smart-placement-portal.pt0axg9.mongodb.net/
MONGODB_NAME=smart_placement_portal
```

---

## Viewing Data in MongoDB Compass

1. **Open MongoDB Compass**
2. **Connect using URI:**
   ```
   mongodb+srv://sadwik1409_db_user:SadwikSimply09@smart-placement-portal.pt0axg9.mongodb.net/
   ```
3. **Select Database:** `smart_placement_portal`
4. **Browse Collections:** View and manage your data

---

## Key Differences from Django ORM

| Feature | Django ORM | MongoDB |
|---------|------------|---------|
| Primary Key | `id` (integer) | `_id` (ObjectId) |
| Relationships | ForeignKey, ManyToMany | Embedded docs or references |
| Queries | `Model.objects.filter()` | `MongoDB.find_many()` |
| Schema | Fixed (migrations) | Flexible (schemaless) |
| Joins | Automatic | Manual or aggregation |

---

## Hybrid Approach

Your application uses both:
- **SQLite/PostgreSQL** (Django ORM) - For Django admin, auth, and built-in features
- **MongoDB** - For application data (jobs, applications, resumes, etc.)

This gives you:
- ✅ Django admin panel
- ✅ Django authentication
- ✅ Flexible MongoDB schema
- ✅ Fast document storage
- ✅ Easy scaling

---

## Testing MongoDB Connection

```bash
cd backend
.\venv\Scripts\python.exe -c "from pymongo import MongoClient; client = MongoClient('mongodb+srv://sadwik1409_db_user:SadwikSimply09@smart-placement-portal.pt0axg9.mongodb.net/'); print('✅ Connected to MongoDB:', client.server_info()['version'])"
```

Expected output:
```
✅ Connected to MongoDB: 8.0.17
```

---

## Next Steps

1. ✅ MongoDB is connected and ready
2. ✅ Utility functions available
3. ✅ Collections defined
4. 🔄 Update views to use MongoDB (optional)
5. 🔄 Migrate existing data to MongoDB (if needed)

---

## Resources

- **MongoDB Python Driver:** https://pymongo.readthedocs.io/
- **MongoDB Compass:** https://www.mongodb.com/products/compass
- **MongoDB Atlas:** https://www.mongodb.com/cloud/atlas

---

**Your MongoDB database is now ready to use!** 🎉

You can start storing data in MongoDB while keeping Django's admin and auth system working with SQLite.
