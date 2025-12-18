from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from django.core.cache import cache


class HealthCheckView(APIView):
    """
    Health check endpoint for monitoring and load balancers.
    Returns system health status including database and cache connectivity.
    """
    permission_classes = []

    def get(self, request):
        health_status = {
            'status': 'healthy',
            'database': 'unknown',
            'cache': 'unknown'
        }
        
        # Check database connection
        try:
            connection.ensure_connection()
            health_status['database'] = 'connected'
        except Exception as e:
            health_status['database'] = 'disconnected'
            health_status['status'] = 'unhealthy'
        
        # Check cache (optional, only if Redis/Memcached configured)
        try:
            cache.set('health_check', 'ok', 10)
            if cache.get('health_check') == 'ok':
                health_status['cache'] = 'connected'
            else:
                health_status['cache'] = 'disconnected'
        except Exception:
            health_status['cache'] = 'not_configured'
        
        status_code = status.HTTP_200_OK if health_status['status'] == 'healthy' else status.HTTP_503_SERVICE_UNAVAILABLE
        
        return Response(health_status, status=status_code)
