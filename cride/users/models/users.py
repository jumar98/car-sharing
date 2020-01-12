from django.db import models
from django.contrib.auth.models import AbstractUser
from cride.utils.models import CSharingModel
from django.core.validators import RegexValidator

class User(CSharingModel, AbstractUser):

    email = models.EmailField(
        'email address',
        unique=True,
        error_messages={
            'unique': 'A use already had use this email.'
        }
    )
    phone_regex = RegexValidator(
        regex=r'\+?1?:\d{9,15}$',
        message="Phone number must be entered in the format: +000000000. Up to 15 digits"
    )
    phone_number = models.CharField(
        max_length=20, blank=True,
        validators=[phone_regex]
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name')

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

    def __str__(self):
        return self.username

    def get_short_name(self):
        return self.username