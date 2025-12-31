from django.urls import path
from .views import RegisterView, LoginView, LogoutView, ProfileUpdateView, CustomPasswordChangeView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileUpdateView.as_view(), name='profile'),
    path('password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
]