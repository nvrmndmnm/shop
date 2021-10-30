from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone_validator = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                     message='Should be a valid phone number.'
                                     )
    phone_number = models.CharField(max_length=17, validators=[phone_validator], unique=True)

