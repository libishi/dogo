# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from rest_framework import serializers, exceptions
from rest_framework.serializers import (HyperlinkedIdentityField,
                                        ModelSerializer,
                                        SerializerMethodField,
                                        ValidationError,
                                        EmailField,
                                        CharField)
from rest_framework_jwt.settings import api_settings
from rest_framework.reverse import reverse as api_reverse
from ..models import UserProfile, Connection

jwt_payload_handler             = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler              = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler    = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER
expire_delta             = api_settings.JWT_REFRESH_EXPIRATION_DELTA
User = get_user_model()


class UserListSerializer(ModelSerializer):
    following = SerializerMethodField()
    follows_requesting_user = SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [
            'user',
            'bio',
            'dog',
            'cat',
            'bird',
            'kennel',
            'breed',
            'age',
            'bio',
            'birth_date',
            'location',
            'following',
            'follows_requesting_user',
        ]

    def get_following(self, obj):
        creator = self.context['request'].user
        following = obj.user
        connected = Connection.objects.filter(creator=creator)
        return len(connected)

    def get_follows_requesting_user(self, obj):
        creator = self.context['request'].user
        following = obj.user
        connected = Connection.objects.filter(following=creator)
        return len(connected)


class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
        ]


class UserLoginSerializer(ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)
    email = EmailField(label="Email Address", required=False, allow_blank=True)

    class Meta:
        model = User
        fields = [
            'email',
            'password',
            'token',
        ]
        extra_kwargs = {
            "password":
                {"write_only":True}
        }

    def validate(self, value):
        user_obj = None
        data = self.get_initial()
        email = data.get("email", None)
        password = data["password"]
        if not email:
            raise ValidationError("Email is required")

        user = User.objects.filter( Q(email=email) ).distinct()
        # passw =  user.first().check_password(password)

        if user:
            if not user.first().check_password(password):
                raise ValidationError("Incorrect password")

        if user.exists() and user.count()==1: #and passw:
            user_obj = user.first()
            payload = jwt_payload_handler(user_obj)
            data["token"] = jwt_encode_handler(payload)
            return data
        else:
            raise ValidationError("This Email is not valid")



        print(data)
        return data






class UserCreateSerializer(ModelSerializer):
    email = EmailField(label="Email")
    email2 = EmailField(label="Re-type Email")
    #password2 = CharField(label="Re-type Password", style={'input_type': 'password'})
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'email2',
            'password',
            #'password2',
        ]
        extra_kwargs = {
            "password":
                {"write_only":True},
            # "password2":
            #     {"write_only": True}
        }

    # def validate_email(self, value):
    #     data = self.get_initial()
    #     email = data.get("email")
    #     user_em = User.objects.filter(email=email)
    #     if user_em.exists():
    #         raise ValidationError("This Email already exists.")
    #     return value

    def validate_username(self, value):
        data = self.get_initial()
        username = data.get("username")
        user_un = User.objects.filter(username=username)
        if user_un.exists():
            raise ValidationError("This Username already exists.")
        return value

    def validate_email2(self, value):
        data = self.get_initial()
        email1 = data.get("email")
        email2 = value
        if email1 != email2:
            raise ValidationError("Emails must match!")
        return value
    #
    # def validate_password2(self, value):
    #     data = self.get_initial()
    #     password = data.get("password")
    #     password2 = value
    #     if password != password2:
    #         raise ValidationError("Passwords must match!")

    def create(self, validated_data):
        # print(validated_data)
        username = validated_data["username"]
        email = validated_data["email"]
        password = validated_data["password"]
        user_obj = User(username=username, email=email)
        user_obj.set_password(password)
        user_obj.save()
        return validated_data




# class ChangePasswordSerializer(ModelSerializer):
#     """
#     Serializer for password change endpoint.
#     """
#     old_password = CharField(required=True)
#     new_password = CharField(required=True)
#
#     class Meta:
#         model = User
#         fields = [
#             'old_password',
#             'new_password',
#         ]
#
#
#     def validate_new_password(self, value):
#         validate_password(value)
#         return value

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128)
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)

    set_password_form_class = SetPasswordForm

    def __init__(self, *args, **kwargs):
        self.old_password_field_enabled = getattr(
            settings, 'OLD_PASSWORD_FIELD_ENABLED', False
        )
        self.logout_on_password_change = getattr(
            settings, 'LOGOUT_ON_PASSWORD_CHANGE', False
        )
        super(PasswordChangeSerializer, self).__init__(*args, **kwargs)

        if not self.old_password_field_enabled:
            self.fields.pop('old_password')

        self.request = self.context.get('request')
        self.user = getattr(self.request, 'user', None)

    def validate_old_password(self, value):
        invalid_password_conditions = (
            self.old_password_field_enabled,
            self.user,
            not self.user.check_password(value)
        )

        if all(invalid_password_conditions):
            raise serializers.ValidationError('Invalid password')
        return value

    def validate(self, attrs):
        self.set_password_form = self.set_password_form_class(
            user=self.user, data=attrs
        )

        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)
        return attrs

    def save(self):
        self.set_password_form.save()
        if not self.logout_on_password_change:
            from django.contrib.auth import update_session_auth_hash
        update_session_auth_hash(self.request, self.user)



