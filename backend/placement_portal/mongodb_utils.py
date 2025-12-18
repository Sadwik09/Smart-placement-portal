"""
MongoDB Database Utilities for Smart Placement Portal
Provides helper functions for MongoDB operations
"""

from django.conf import settings
from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime


class MongoDB:
    """MongoDB connection and operations helper"""
    
    _client = None
    _db = None
    
    @classmethod
    def get_client(cls):
        """Get or create MongoDB client"""
        if cls._client is None:
            cls._client = MongoClient(settings.MONGODB_URI)
        return cls._client
    
    @classmethod
    def get_database(cls):
        """Get or create MongoDB database"""
        if cls._db is None:
            client = cls.get_client()
            cls._db = client[settings.MONGODB_NAME]
        return cls._db
    
    @classmethod
    def get_collection(cls, collection_name):
        """Get a specific collection"""
        db = cls.get_database()
        return db[collection_name]
    
    @classmethod
    def insert_one(cls, collection_name, document):
        """Insert a single document"""
        collection = cls.get_collection(collection_name)
        document['created_at'] = datetime.datetime.utcnow()
        document['updated_at'] = datetime.datetime.utcnow()
        result = collection.insert_one(document)
        return str(result.inserted_id)
    
    @classmethod
    def insert_many(cls, collection_name, documents):
        """Insert multiple documents"""
        collection = cls.get_collection(collection_name)
        now = datetime.datetime.utcnow()
        for doc in documents:
            doc['created_at'] = now
            doc['updated_at'] = now
        result = collection.insert_many(documents)
        return [str(id) for id in result.inserted_ids]
    
    @classmethod
    def find_one(cls, collection_name, query, **kwargs):
        """Find a single document"""
        collection = cls.get_collection(collection_name)
        if '_id' in query and isinstance(query['_id'], str):
            query['_id'] = ObjectId(query['_id'])
        return collection.find_one(query, **kwargs)
    
    @classmethod
    def find_many(cls, collection_name, query=None, **kwargs):
        """Find multiple documents"""
        collection = cls.get_collection(collection_name)
        if query is None:
            query = {}
        if '_id' in query and isinstance(query['_id'], str):
            query['_id'] = ObjectId(query['_id'])
        return list(collection.find(query, **kwargs))
    
    @classmethod
    def update_one(cls, collection_name, query, update, upsert=False):
        """Update a single document"""
        collection = cls.get_collection(collection_name)
        if '_id' in query and isinstance(query['_id'], str):
            query['_id'] = ObjectId(query['_id'])
        
        # Add updated_at timestamp
        if '$set' in update:
            update['$set']['updated_at'] = datetime.datetime.utcnow()
        else:
            update['$set'] = {'updated_at': datetime.datetime.utcnow()}
        
        result = collection.update_one(query, update, upsert=upsert)
        return result.modified_count
    
    @classmethod
    def update_many(cls, collection_name, query, update):
        """Update multiple documents"""
        collection = cls.get_collection(collection_name)
        if '_id' in query and isinstance(query['_id'], str):
            query['_id'] = ObjectId(query['_id'])
        
        # Add updated_at timestamp
        if '$set' in update:
            update['$set']['updated_at'] = datetime.datetime.utcnow()
        else:
            update['$set'] = {'updated_at': datetime.datetime.utcnow()}
        
        result = collection.update_many(query, update)
        return result.modified_count
    
    @classmethod
    def delete_one(cls, collection_name, query):
        """Delete a single document"""
        collection = cls.get_collection(collection_name)
        if '_id' in query and isinstance(query['_id'], str):
            query['_id'] = ObjectId(query['_id'])
        result = collection.delete_one(query)
        return result.deleted_count
    
    @classmethod
    def delete_many(cls, collection_name, query):
        """Delete multiple documents"""
        collection = cls.get_collection(collection_name)
        if '_id' in query and isinstance(query['_id'], str):
            query['_id'] = ObjectId(query['_id'])
        result = collection.delete_many(query)
        return result.deleted_count
    
    @classmethod
    def count_documents(cls, collection_name, query=None):
        """Count documents matching query"""
        collection = cls.get_collection(collection_name)
        if query is None:
            query = {}
        return collection.count_documents(query)
    
    @classmethod
    def aggregate(cls, collection_name, pipeline):
        """Run aggregation pipeline"""
        collection = cls.get_collection(collection_name)
        return list(collection.aggregate(pipeline))


# Collection names (constants)
class Collections:
    """MongoDB collection names"""
    USERS = 'users'
    STUDENTS = 'students'
    RECRUITERS = 'recruiters'
    JOBS = 'jobs'
    APPLICATIONS = 'applications'
    RESUMES = 'resumes'
    INTERVIEWS = 'interviews'
    NOTIFICATIONS = 'notifications'
    ANALYTICS = 'analytics'


# Helper functions for common operations
def serialize_mongo_doc(doc):
    """Convert MongoDB document to JSON-serializable dict"""
    if doc is None:
        return None
    if isinstance(doc, list):
        return [serialize_mongo_doc(item) for item in doc]
    if isinstance(doc, dict):
        result = {}
        for key, value in doc.items():
            if isinstance(value, ObjectId):
                result[key] = str(value)
            elif isinstance(value, datetime.datetime):
                result[key] = value.isoformat()
            elif isinstance(value, dict):
                result[key] = serialize_mongo_doc(value)
            elif isinstance(value, list):
                result[key] = [serialize_mongo_doc(item) for item in value]
            else:
                result[key] = value
        return result
    return doc


def get_or_create_indexes():
    """Create MongoDB indexes for better performance"""
    db = MongoDB.get_database()
    
    # Users collection indexes
    db[Collections.USERS].create_index('email', unique=True)
    db[Collections.USERS].create_index('username', unique=True)
    
    # Jobs collection indexes
    db[Collections.JOBS].create_index('company_name')
    db[Collections.JOBS].create_index('posted_by')
    db[Collections.JOBS].create_index('is_active')
    
    # Applications collection indexes
    db[Collections.APPLICATIONS].create_index('job_id')
    db[Collections.APPLICATIONS].create_index('student_id')
    db[Collections.APPLICATIONS].create_index('status')
    
    # Notifications collection indexes
    db[Collections.NOTIFICATIONS].create_index('user_id')
    db[Collections.NOTIFICATIONS].create_index('is_read')
    
    print("✅ MongoDB indexes created successfully")
