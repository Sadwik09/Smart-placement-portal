from rest_framework import serializers
from analytics.models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'type', 'is_read', 'created_at', 'related_id']
        read_only_fields = ['id', 'created_at']
