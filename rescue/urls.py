from django.urls import path
from django.contrib.auth import views as auth_views
from django.http import JsonResponse
from . import views

def health_check(request):
    """Simple health check endpoint"""
    return JsonResponse({
        'status': 'ok',
        'django': 'working',
        'database': 'checking...'
    })

urlpatterns = [
    path('health/', health_check, name='health'),
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='rescue/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Animals
    path('animals/', views.animal_list, name='animal_list'),
    path('animals/<int:pk>/', views.animal_detail, name='animal_detail'),
    path('animals/create/', views.animal_create, name='animal_create'),
    path('animals/<int:pk>/edit/', views.animal_edit, name='animal_edit'),
    
    # Reports
    path('reports/', views.report_list, name='report_list'),
    path('reports/create/', views.report_create, name='report_create'),
    path('reports/<int:pk>/', views.report_detail, name='report_detail'),
    
    # Adoption
    path('animals/<int:animal_pk>/adopt/', views.adoption_request_create, name='adoption_request_create'),
    path('adoption-requests/<int:pk>/manage/', views.adoption_request_manage, name='adoption_request_manage'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('shelter/create/', views.shelter_create, name='shelter_create'),
    
    # Updates
    path('animals/<int:animal_pk>/update/', views.update_create, name='update_create_animal'),
    path('reports/<int:report_pk>/update/', views.update_create, name='update_create_report'),
    
    # Notifications
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/<int:notification_id>/read/', views.notification_mark_read, name='notification_mark_read'),
    path('notifications/mark-all-read/', views.notification_mark_all_read, name='notification_mark_all_read'),
]


