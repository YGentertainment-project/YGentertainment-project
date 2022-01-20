from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt

app_name = 'account'

urlpatterns = [
    path('', base, name='base'),
    path("api/login/", csrf_exempt(UserLoginAPI.as_view()), name="user_login_api"),
    path("api/simplelogin/", csrf_exempt(UserSimpleLoginAPI.as_view()), name="user_simple_login_api"),
    path("api/logout/", UserLogoutAPI.as_view(), name="user_logout_api"),
    path("api/register/", csrf_exempt(UserRegisterAPI.as_view()), name="user_register_api"),
    path("api/change_password/", UserChangePasswordAPI.as_view(), name="user_change_password_api"),
]
