"""
Management command to initialize MongoDB collections and indexes
"""
from django.core.management.base import BaseCommand
from placement_portal.mongodb_utils import MongoDB, Collections, get_or_create_indexes


class Command(BaseCommand):
    help = 'Initialize MongoDB collections and create indexes'

    def handle(self, *args, **options):
        self.stdout.write('Initializing MongoDB...')
        
        try:
            # Test connection
            db = MongoDB.get_database()
            self.stdout.write(self.style.SUCCESS(f'✅ Connected to MongoDB: {db.name}'))
            
            # List existing collections
            collections = db.list_collection_names()
            self.stdout.write(f'Existing collections: {collections if collections else "None"}')
            
            # Create indexes
            self.stdout.write('Creating indexes...')
            get_or_create_indexes()
            
            # Verify collections
            collections = db.list_collection_names()
            self.stdout.write(self.style.SUCCESS(f'✅ MongoDB initialized successfully'))
            self.stdout.write(f'Available collections: {collections}')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error initializing MongoDB: {e}'))
