from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('complaints/', views.complaint_list, name='complaint_list'),
    path('complaints/new/', views.file_complaint, name='file_complaint'),
    path('complaints/<int:pk>/', views.complaint_detail, name='complaint_detail'),
    path('complaints/<int:pk>/resolve/', views.add_resolution, name='add_resolution'),
    path('complaints/<int:pk>/feedback/', views.add_feedback, name='add_feedback'),
    path('complaints/<int:pk>/assign/', views.assign_complaint, name='assign_complaint'),
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/<int:pk>/read/', views.mark_notification_read, name='mark_notification_read'),
    path('admin-overview/', views.admin_overview, name='admin_overview'),
]
