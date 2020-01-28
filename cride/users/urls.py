from django.urls import path
from cride.users.views import (
    UserLoginAPIView, 
    UserSignUpAPIView,
    AccountVerificationView
)

urlpatterns = [
    path('users/login/', UserLoginAPIView.as_view(), name='login'),
    path('users/signup/', UserSignUpAPIView.as_view(), name='signup'),
    path('users/verify/', AccountVerificationView.as_view(), name='verify'),
]