from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('curso/<slug:slug>/', views.course_detail, name='course_detail'),
    path('curso/<slug:slug>/certificado/', views.course_certificate, name='course_certificate'),
    path('curso/<slug:course_slug>/leccion/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('curso/<slug:course_slug>/leccion/<int:lesson_id>/completar/', views.toggle_lesson_completed, name='toggle_completed'),
    
    path('kdemia-admin/', views.kdemia_admin_dashboard, name='kdemia_admin'),
    path('api/tuzy/', views.ask_tuzy, name='ask_tuzy'),

    # Autenticación
    path('login/', views.login_view, name='login'),
    path('registro/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
]