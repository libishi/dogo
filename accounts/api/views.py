# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import get_user_model
from rest_framework.generics import (ListAPIView, RetrieveUpdateAPIView, RetrieveAPIView, DestroyAPIView, CreateAPIView, GenericAPIView)
from rest_framework.permissions import (IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny)
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from .serializers import UserCreateSerializer, UserLoginSerializer, UserDetailSerializer, UserListSerializer,PasswordChangeSerializer
#from .permissions import IsOwnerOrReadOnly
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.utils.decorators import method_decorator
from django.contrib.auth.views import password_reset, password_reset_confirm
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from datetime import datetime
from django.views.decorators.debug import sensitive_post_parameters
from accounts.models import UserProfile

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters(
        'password', 'old_password', 'new_password1', 'new_password2'
    )
)

User = get_user_model()

class UserListAPIView(ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [AllowAny]

class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

class UserDetailsAPIView(APIView):
    serializer_class = UserDetailSerializer
    queryset = User.objects.all()
    #permission_classes = [AllowAny]

    def get(self, request):
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)
        print(serializer.data)

class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class UserLogoutAPIView(APIView):
#     queryset = User.objects.all()
#     permission_classes = [AllowAny]
#
    def get(self, request, format=None):
#         Token.objects.create(user=get_user_model())
#         Token.objects.get(user=user)
#         if Token.objects.filter(user=user).exist():
            request.user.auth_token.delete()
            return Response(status=status.HTTP_200_OK)
#         else:
#             return Response(status=status.HTTP_400_BAD_REQUEST)

# class UpdatePassword(APIView):
#     """
#     An endpoint for changing password.
#     """
#     serializer_class = ChangePasswordSerializer
#     permission_classes = [AllowAny]
#
#     def get(self, request):
#         serializer = ChangePasswordSerializer(request.user)
#         return Response(serializer.data)
#         print(serializer.data)
#
#     def get_object(self, queryset=None):
#         return self.request.user
#
#     def put(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         serializer = ChangePasswordSerializer(data=request.data)
#
#         if serializer.is_valid():
#             # Check old password
#             old_password = serializer.data.get("old_password")
#             if not self.object.check_password(old_password):
#                 return Response({"old_password": ["Wrong password."]},
#                                 status=status.HTTP_400_BAD_REQUEST)
#             # set_password also hashes the password that the user will get
#             self.object.set_password(serializer.data.get("new_password"))
#             self.object.save()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordChangeView(GenericAPIView):
    """
    Calls Django Auth SetPasswordForm save method.
    Accepts the following POST parameters: new_password1, new_password2
    Returns the success/fail message.
    """
    serializer_class = PasswordChangeSerializer
    permission_classes = [AllowAny]

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(PasswordChangeView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": ("New password has been saved.")})
