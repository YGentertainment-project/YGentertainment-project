import re

from django.contrib import auth
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from drf_yasg.utils import swagger_auto_schema

from utils.api import APIView, validate_serializer
from utils.shortcuts import rand_str
from utils.decorators import login_required
from models import User, UserProfile
from serializers import *


class UserProfileAPI(APIView):
    @method_decorator(ensure_csrf_cookie)
    def get(self, request, **kwargs):
        """
        Determine whether to log in, and return user information if logged in
        """
        user = request.user
        if not user.is_authenticated:
            return self.success()
        show_real_name = False
        username = request.GET.get("username")
        try:
            if username:
                user = User.objects.get(username=username, is_disabled=False)
            else:
                user = request.user
                # The api returns your own information, you can return real_name
                show_real_name = True
        except User.DoesNotExist:
            return self.error("User does not exist")
        return self.success(UserProfileSerializer(user.userprofile, show_real_name=show_real_name).data)

    @login_required
    def put(self, request):
        data = request.data
        user_profile = request.user.userprofile
        for k, v in data.items():
            setattr(user_profile, k, v)
        user_profile.save()
        return self.success(UserProfileSerializer(user_profile, show_real_name=True).data)


class UserLoginAPI(APIView):
    @validate_serializer(UserLoginSerializer)
    def post(self, request):
        """
        User login api
        """
        data = request.data
        user = auth.authenticate(username=data["username"], password=data["password"])
        # None is returned if username or password is wrong
        if not user:
            return self.error("Invalid username or password")
        if user.is_disabled:
            return self.error("Your account has been disabled")
        if not user.has_email_auth:
            return self.error("Your need to authenticate your email")
        auth.login(request, user)
        return self.success("Succeeded")


class UserLogoutAPI(APIView):
    def get(self, request):
        auth.logout(request)
        return self.success()


class UserRegisterAPI(APIView):
    @validate_serializer(UserRegisterSerializer)
    def post(self, request):
        """
        User register api
        """

        data = request.data
        data["username"] = data["username"].lower()
        data["email"] = data["email"].lower()
        if User.objects.filter(username=data["username"]).exists():
            return self.error("Username already exists")
        if not re.match(r"^20[0-9]{8}$", data["username"]):
            return self.error("Not student ID")
        if User.objects.filter(email=data["email"]).exists():
            return self.error("Email already exists")
        if data["email"].split("@")[1] not in ("g.skku.edu", "skku.edu"):
            return self.error("Invalid domain (Use skku.edu or g.skku.edu)")
        user = User.objects.create(username=data["username"], email=data["email"], major=data["major"])
        user.set_password(data["password"])
        user.has_email_auth = False
        user.email_auth_token = rand_str()
        user.save()

        UserProfile.objects.create(user=user)

        render_data = {
            "username": user.username,
        }

        return self.success("Succeeded")


class UserChangePasswordAPI(APIView):
    @validate_serializer(UserChangePasswordSerializer)
    @login_required
    def post(self, request):
        """
        User change password api
        """
        data = request.data
        username = request.user.username
        user = auth.authenticate(username=username, password=data["old_password"])
        if not user:
            return self.error("Invalid old password")
        user.set_password(data["new_password"])
        user.save()
        return self.success("Succeeded")
