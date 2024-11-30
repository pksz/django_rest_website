from django.urls import path
from .views import UserSignupView, CustomAuthToken

#urls

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='user-signup'),
    path('login/', CustomAuthToken.as_view(), name='user-login'),
]