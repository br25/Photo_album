from django.urls import path
from .views import UserView, RegistrationView, LoginView, LogoutView

urlpatterns = [
    path('users/', UserView.as_view(), name='users'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
