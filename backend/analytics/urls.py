from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdminDashboardView, UserApprovalView, PlacementStatisticsView
from .notification_views import NotificationViewSet

router = DefaultRouter()
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    # Router endpoints under /api/analytics/
    path('', include(router.urls)),

    # Analytics endpoints (mounted at /api/analytics/)
    path('dashboard/', AdminDashboardView.as_view(), name='admin-dashboard'),
    path('approvals/', UserApprovalView.as_view(), name='user-approvals'),
    path('approvals/<int:user_id>/approve/', UserApprovalView.as_view(), name='approve-user'),
    path('statistics/', PlacementStatisticsView.as_view(), name='placement-statistics'),
]
