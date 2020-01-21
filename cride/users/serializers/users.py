
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.response import Response 
from rest_framework.authtoken.models import Token
from cride.users.models import User

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

