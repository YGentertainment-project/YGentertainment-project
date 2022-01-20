from rest_framework import serializers

from .models import AdminType, User


class UserLoginSerializer(serializers.Serializer):
    # if we use YG Login api, should modify this part
    username = serializers.CharField()
    password = serializers.CharField()


class UsernameOrEmailCheckSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)


class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=32)
    password = serializers.CharField(min_length=6)
    email = serializers.EmailField(max_length=64)
    captcha = serializers.CharField()


class EmailAuthSerializer(serializers.Serializer):
    token = serializers.CharField()


class UserChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField(min_length=8)


class UserChangeEmailSerializer(serializers.Serializer):
    password = serializers.CharField()
    new_email = serializers.EmailField(max_length=64)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "major", "admin_type", "problem_permission",
                  "create_time", "last_login", "is_disabled"]


class EditUserSerializer(serializers.Serializer):
    # for super admin and admin
    id = serializers.IntegerField()
    username = serializers.CharField(max_length=32)
    password = serializers.CharField(min_length=6, allow_blank=True, required=False, default=None)
    email = serializers.EmailField(max_length=64)
    admin_type = serializers.ChoiceField(choices=(AdminType.REGULAR_USER, AdminType.ADMIN, AdminType.SUPER_ADMIN))
    is_disabled = serializers.BooleanField()
