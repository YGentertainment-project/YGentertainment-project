app_name = 'account'


from django.urls import path

from .views import *

urlpatterns = [
    path("login/", UserLoginAPI.as_view(), name="user_login_api"),
    path("logout/", UserLogoutAPI.as_view(), name="user_logout_api"),
    path("register/", UserRegisterAPI.as_view(), name="user_register_api"),
    path("change_password/", UserChangePasswordAPI.as_view(), name="user_change_password_api"),
]