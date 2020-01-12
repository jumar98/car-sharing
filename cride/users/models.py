 
from django.db import models
from django.contrib.auth.models import AbstractUser
from cride.utils.models import CSharingModel

class User(CSharingModel, AbstractUser):

    email = models.EmailField(
        'email_address',
        unique=True,
        error_message={
            'unique': 'A use already had use this email.'
        }
    )
    phone_number = models.CharField(max_length=20, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = {'username', 'first_name', 'last_name'}

    is_client = models.BooleanField(
        'client',
        default=True,
        help_text=(
            'This help to differentiate the users and performs queries.'
            'Clients are the main type of users.'
        )
    )

    is_verified = models.BooleanField(
        'verified',
        default=False,
        help_text='Set to true when the user has verified its email address.'
    )