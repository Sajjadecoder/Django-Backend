from django.db import models

# Create your models here.
import uuid
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager
)

class UserManager(BaseUserManager):
    def create_user(self,email,password = None,**extra_fields):
        if not email:
            raise ValueError('Email required')
        norm_email =self.normalize_email(email)
        user = self.model(email=norm_email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser,PermissionsMixin):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150)
    is_active = models.BooleanField(default=False)        
    is_staff = models.BooleanField(default=False)        
    date_joined = models.DateTimeField(auto_now_add=True)
    objects = UserManager ()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']
    EMAIL_FIELD = 'email'
    
    def __str__(self):
        return self.email