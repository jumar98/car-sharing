
from rest_framework import serializers
from django.contrib.auth import password_validation, authenticate
from rest_framework.response import Response 
from rest_framework.authtoken.models import Token
from cride.users.models import User, Profile
from rest_framework.validators import UniqueValidator
from django.core.mail import EmailMultiAlternatives
from django.core.validators import RegexValidator
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
import jwt
from cride.users.serializers.profile import ProfileModelSerializer

class UserModelSerializer(serializers.ModelSerializer):

    profile = ProfileModelSerializer(read_only=True)

    class Meta:

        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'profile'
        )

class UserLoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=70)

    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid credentials.')
        if not user.is_verified:
            raise serializers.ValidationError("Account isn't active yet.") 
        self.context['user'] = user
        return data

    def create(self, data):
        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key

class UserSignUpSerializer(serializers.Serializer):

    email = serializers.EmailField(
       validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        min_length=6,
        max_length=30,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: +000000000. Up to 15 digits"
    )
    phone_number = serializers.CharField(
        validators=[phone_regex]
    )
    password = serializers.CharField(min_length=6, max_length=70)
    password_confirmation = serializers.CharField(min_length=6, max_length=70)
    first_name = serializers.CharField(min_length=5, max_length=100)
    last_name = serializers.CharField(min_length=5, max_length=100)
    
    def validate(self, data):
        passwd = data['password']
        passwd_conf = data['password_confirmation']
        if passwd != data['password_confirmation']:
            raise serializers.ValidationError("Password, didn't match")
        password_validation.validate_password(passwd)
        return data

    def create(self, data):
        data.pop('password_confirmation')
        user = User.objects.create_user(**data, is_verified=False, is_client=True)
        profile = Profile.objects.create(user=user)
        self.send_confirmation_email(user)
        return user

    def send_confirmation_email(self, user):
        verification_token = self.get_verification_token(user)
        subject = "Welcom @{}! verify your account plesae.".format(user.username)
        from_email = 'noreply@example.com',
        content = render_to_string(
            'emails/users/account_verification.html',
            {'token': verification_token, 'user':user}
        )
        msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
        msg.attach_alternative(content, "text/html")
        msg.send()

    def get_verification_token(self, user):
        exp_date = timezone.now() + timedelta(days=3)
        payload = {
            'username': user.username,
            'exp': int(exp_date.timestamp()),
            'type': 'email_confirmation'
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token.decode()

class AccountVerificationSerializer(serializers.Serializer):

    token = serializers.CharField()

    def validate_token(self, data):
        try:
            payload = jwt.decode(data, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return serializers.ValidationError("Verification time it has expired.")
        except jwt.PyJWTError:
            raise serializers.ValidationError('Invalid token')
        if payload['type'] in "email_confirmaton":
            raise serializers.ValidationError("Invalid token")

        self.context['payload'] = payload
        return data
    
    def save(self):

        payload = self.context['payload']
        user = User.objects.get(username=payload['username'])
        user.is_verified = True
        user.save()

