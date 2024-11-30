from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


#user fields here
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)