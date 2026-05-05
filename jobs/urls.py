from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'jobs', views.JobApplicationViewSet, basename='job')
urlpatterns = [
    path('', include(router.urls))    
    # path('jobs/', views.job_list.as_view(), name='job-list'),
    # path('jobs/<int:pk>/', views.job_detail.as_view(), name='job-detail')
]
