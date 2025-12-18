from django.urls import path
from .views import StudentProfileView, StudentListView

urlpatterns = [
    path('profile/', StudentProfileView.as_view(), name='student-profile'),
    path('list/', StudentListView.as_view(), name='student-list'),
]
