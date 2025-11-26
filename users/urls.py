from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),  # Теперь обрабатывает GET и POST
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
]
