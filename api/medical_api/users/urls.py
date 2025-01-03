from django.urls import path
from users import views

from .views import RegistrationView, LoginView
urlpatterns = [
    path('auth/register/', RegistrationView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
]