
from rest_framework import serializers
from django.contrib.auth import password_validation, authenticate
from rest_framework.response import Response 
from rest_framework.authtoken.models import Token
from cride.users.models import User, Profile
from rest_framework.validators import UniqueValidator 
from django.core.validators import RegexValidator

class UserModelSerializer(serializers.ModelSerializer):

    class Meta:

        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number'

        )

class UserLoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=70)

    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid credention.')
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
        user = User.objects.create_user(**data)
        profile = Profile.objects.create(user=user)
        return user

