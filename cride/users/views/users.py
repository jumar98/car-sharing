
from rest_framework.views import APIView
from rest_framework import status
from cride.users.serializers import (
    UserLoginSerializer, 
    UserModelSerializer,
    UserSignUpSerializer,
    AccountVerificationSerializer
)
from rest_framework.response import Response

class UserLoginAPIView(APIView):

    def post(self, request, *args, **kwargs):

        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'access_token': token
        }
        return Response(data, status=status.HTTP_201_CREATED)

class UserSignUpAPIView(APIView):

    def post(self, request, *args, **kwargs):
        
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)


class AccountVerificationView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = AccountVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {'message': 'Congratulations all is well.'}
        return Response(data, status=status.HTTP_200_OK)