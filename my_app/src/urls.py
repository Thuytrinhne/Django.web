from django.urls import path
from . import views

urlpatterns = [
    path('', views.overall_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('overall/', views.overall_view, name='overall'),
    path('modelling/', views.modelling_view, name='modelling'),
    path('logout/', views.logout_view, name='logout'),
]