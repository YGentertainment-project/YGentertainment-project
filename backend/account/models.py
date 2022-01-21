from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.db import models


class AdminType(object):
    REGULAR_USER = "Regular User"
    ADMIN = "Admin"
    SUPER_ADMIN = "Super Admin"


class User(AbstractBaseUser):
    username = models.TextField(unique=True, max_length=100)
    yg_email = models.TextField(unique=True)
    create_time = models.DateTimeField(auto_now_add=True, null=True)
    is_disabled = models.BooleanField(default=False)
    has_email_auth = models.BooleanField(default=True)
    email_auth_token = models.TextField(null=True)
    # After negotiate, one of UserType
    admin_type = models.TextField(default=AdminType.REGULAR_USER)

    objects = UserManager()

    def is_admin(self):
        return self.admin_type == AdminType.ADMIN

    def is_super_admin(self):
        return self.admin_type == AdminType.SUPER_ADMIN

    def is_admin_role(self):
        return self.admin_type in [AdminType.ADMIN, AdminType.SUPER_ADMIN]

    class Meta:
        db_table = "user"
