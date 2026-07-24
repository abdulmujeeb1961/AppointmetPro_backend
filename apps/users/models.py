# If we use AbstractUser we can use the default user model. There is no need to create username, password, email, first_name, last_name,is_superuser, is_staff, is_active. In settings we have to add AUTH_USER_MODEL = 'users.User' and in installed_apps we have to add 'apps.users.apps.UsersConfig'

from django.db import models
from django.contrib.auth.models import AbstractUser

SUPER_ADMIN = 'SUPER_ADMIN'
BUSINESS_OWNER='BUSINESS_OWNER'
STAFF = 'STAFF'

ROLE_CHOICES = [
    (SUPER_ADMIN, 'Super Admin'),
    (BUSINESS_OWNER, 'Business Owner'),
    (STAFF, 'Staff'),
]
class User(AbstractUser):
    mobile_number = models.CharField(max_length=10,unique=True)
    role=models.CharField(max_length=30,choices=ROLE_CHOICES,default=STAFF)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    is_mobile_verified=models.BooleanField(default=False)
    
    def __str__(self):
         return f"{self.username} - {self.role}"


