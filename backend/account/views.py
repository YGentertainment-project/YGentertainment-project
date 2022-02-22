import re

from django.contrib import auth
from django.shortcuts import redirect, render

from rest_framework.views import APIView
from utils.api import APIView, validate_serializer
from utils.shortcuts import rand_str
from utils.decorators import login_required
from .models import User
from .serializers import *


# 정의 : base
# 목적 : 웹 페이지 시작 페이지 로딩 
# 멤버함수 : 
# 개발자 : 김민희, minheekim3@naver.com
# 최종수정일 : 2022-02-22
def base(request):
    return render(request, 'account/main.html')


# 정의 : user simple login api
# 목적 : default 정보를 이용한 형식적인 simple login 구현
# 멤버함수 : 
# 개발자 : 김민희, minheekim3@naver.com
# 최종수정일 : 2022-02-22
class UserSimpleLoginAPI(APIView):
    def get(self, request):
        '''
        User simple login api
        '''
        # default id and pw
        username = 'yg'
        password = 'ygenter1234'
        yg_email = 'ygenter@mail.com'
        if User.objects.filter(username=username).exists():
            # 이미 존재하는 username -> 로그인
            user = User.objects.filter(username=username).first()
            auth.login(request, user)
        elif User.objects.filter(yg_email=yg_email).exists():
            # 이미 존재하는 email -> 로그인
            user = User.objects.filter(yg_email=yg_email).first()
            auth.login(request, user)
        else:
            # 새롭게 register
            user = User.objects.create(username=username, yg_email=yg_email, password=password)
            user.has_email_auth = False
            user.email_auth_token = rand_str()
            user.save()
            # register 후 login
            auth.login(request, user)
        response = redirect('dataprocess:daily')
        # 로그인 정보를 web cookie에 저장
        response.set_cookie('username', username)
        return response


# 정의 : user simple logout api
# 목적 : simple login으로부터 로그아웃
# 멤버함수 : 
# 개발자 : 김민희, minheekim3@naver.com
# 최종수정일 : 2022-02-22
class UserLogoutAPI(APIView):
    def get(self, request):
        '''
        User simple logout api
        '''
        auth.logout(request)
        response = redirect('dataprocess:base')
        # 로그인 정보를 web cookie에서 삭제
        response.delete_cookie('username')
        return response


# 정의 : 
# 목적 : 
# 멤버함수 : 
# 개발자 : 
# 최종수정일 : 
class UserLoginAPI(APIView):
    @validate_serializer(UserLoginSerializer)
    def post(self, request):
        '''
        User login api
        현재 사용x
        '''
        data = request.data
        user = auth.authenticate(username=data['username'], password=data['password'])
        # None is returned if username or password is wrong
        if not user:
            return self.error("Invalid username or password")
        if user.is_disabled:
            return self.error("Your account has been disabled")
        if not user.has_email_auth:
            return self.error("Your need to authenticate your email")
        auth.login(request, user)
        return self.success("Succeeded")


# 정의 : 
# 목적 : 
# 멤버함수 : 
# 개발자 : 
# 최종수정일 : 
class UserRegisterAPI(APIView):
    @validate_serializer(UserRegisterSerializer)
    def post(self, request):
        '''
        User register api
        현재 사용x
        '''
        data = request.data
        data["username"] = data["username"].lower()
        data["email"] = data["email"].lower()
        if User.objects.filter(username=data["username"]).exists():
            return self.error("Username already exists")
        if not re.match(r"^20[0-9]{8}$", data["username"]):
            return self.error("Not student ID")
        if User.objects.filter(yg_email=data["email"]).exists():
            return self.error("Email already exists")
        if data["email"].split("@")[1] not in ("g.skku.edu", "skku.edu"):
            return self.error("Invalid domain (Use skku.edu or g.skku.edu)")
        user = User.objects.create(username=data["username"], yg_email=data["email"])
        user.set_password(data["password"])
        user.has_email_auth = False
        user.email_auth_token = rand_str()
        user.save()

        return self.success("Succeeded")


# 정의 : 
# 목적 : 
# 멤버함수 : 
# 개발자 : 
# 최종수정일 : 
class UserChangePasswordAPI(APIView):
    @validate_serializer(UserChangePasswordSerializer)
    @login_required
    def post(self, request):
        '''
        User change password api
        현재 사용x
        '''
        data = request.data
        username = request.user.username
        user = auth.authenticate(username=username, password=data["old_password"])
        if not user:
            return self.error("Invalid old password")
        user.set_password(data["new_password"])
        user.save()
        return self.success("Succeeded")
