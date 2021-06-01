from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('',home, name="home" ),
    path('login',login_attempt, name="login" ),
    path('register',register_attempt, name="register" ),
    path('success',success, name="success" ),
    path('token',token_send, name="token_send" ),
    path('verify/<auth_token>',verify, name="verify" ),
    path('error',error_page, name="error" ),
    path('logout',logout_request, name="logout" ),
]