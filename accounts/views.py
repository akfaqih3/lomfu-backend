from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import (
    UserInputSerializer,
    UserOutputSerializer,
    UserUpdateSerializer,
    OTPSendSerializer,
    OTPVerifySerializer,
)

from .services import (
    user_create,
    user_update,
    user_delete,
    send_otp,
    verify_otp,
)
from .selectors import (
    user_by_id,
)
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

User = get_user_model()


class UserCreateAPI(APIView):
    serializer_class = UserInputSerializer
    def post(self, request):
        serializer =self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = user_create(
                serializer.data['name'],
                serializer.data['email'],
                serializer.data['role'],
                serializer.data['password'],
                serializer.data['phone'] if 'phone' in serializer.data else None 
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAPI(APIView):
    serializer_class = UserOutputSerializer
    def get(self, request, id):
        user = user_by_id(id)
        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(UserOutputSerializer(user).data, status=status.HTTP_200_OK)
    

class UserUpdateAPI(APIView):
    serializer_class = UserUpdateSerializer
    def put(self, request, id):
        user = user_by_id(id)
        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = user_update(
                user,
                serializer.data['name'] if 'name' in serializer.data else user.name,
                serializer.data['email'] if 'email' in serializer.data else user.email,
                serializer.data['role'] if 'role' in serializer.data else user.role,
                serializer.data['phone'] if 'phone' in serializer.data else user.phone,
                serializer.data['photo'] if 'photo' in serializer.data else user.profile.photo,
                serializer.data['bio'] if 'bio' in serializer.data else user.profile.bio,
            )
            return Response(UserOutputSerializer(user).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDeleteAPI(APIView):
    def delete(self, request, id):
        user = user_by_id(id)
        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if user_delete(user):
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    


    
class OTPSendAPI(APIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = OTPSendSerializer
    def post(self, request):
        serializer = OTPSendSerializer(data=request.data)
        if serializer.is_valid():
            if send_otp(serializer.data["email"]):
                return Response({"message": "OTP sent successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OTPVerifyAPI(APIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = OTPVerifySerializer
    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        if serializer.is_valid():
            if verify_otp(serializer.data["email"],serializer.data["otp"]):
                user = get_object_or_404(User, email=serializer.data["email"])
                refresh = RefreshToken.for_user(user)
                token = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                }
                return Response(token, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
