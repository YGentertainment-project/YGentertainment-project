from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt

app_name = 'account'

urlpatterns = [
    path("login/", csrf_exempt(UserLoginAPI.as_view()), name="user_login_api"),
    path("simplelogin/", csrf_exempt(UserSimpleLoginAPI.as_view()), name="user_simple_login_api"),
    path("logout/", UserLogoutAPI.as_view(), name="user_logout_api"),
    path("register/", csrf_exempt(UserRegisterAPI.as_view()), name="user_register_api"),
    path("change_password/", UserChangePasswordAPI.as_view(), name="user_change_password_api"),
]