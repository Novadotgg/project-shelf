from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),               # Homepage
    path('register/', views.register_user, name='register'),  # Signup for creator
    path('login/', views.user_login, name='login'),      # Login
    path('logout/', views.user_logout, name='logout'),   # Logout
    path('demo_home/', views.demo_home, name='demo_home'),  # After login
    path('creator_dashboard/', views.creator_dashboard_view, name='creator_dashboard'),  # Creator dashboard
    path('dash/', views.creator_analytics_dashboard, name='dash'),  # Visitor dashboardpath('creators/', views.creator_list_view, name='creator_list'),
    path('creators/<str:username>/', views.creator_profile_view, name='creator_profile'),
    path('creators/', views.creator_list_view, name='creator_list'),  # List of creators
    path('visitor_dashboard/', views.visitor_dashboard_view, name='visitor_dashboard'),  # Visitor dashboard
    path('project/<int:project_id>/visit/', views.project_redirect_view, name='project_redirect'),
    path('track_click/<int:project_id>/', views.track_click_view, name='track_click'),



]