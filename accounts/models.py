from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True, null=False, blank=False)

    is_customer = models.BooleanField(default=False)
    is_support_engineer = models.BooleanField(default=False)
    
