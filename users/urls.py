from django.urls import path

from .views import SignUpView, profile

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='user_signup'),
    path('profile/', profile, name='user_profile'),
]
