# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url, include
from .views import (UserListAPIView, UserCreateAPIView, UserLoginAPIView, UserLogoutAPIView, UserDetailsAPIView, PasswordChangeView)#, reset_confirm, reset, password_reset_confirm)
from django.views.generic import TemplateView
# from djoser.views import PasswordResetConfirmView
# from django.contrib.auth import views as auth_views
urlpatterns = [
    url(r'^register/$', UserCreateAPIView.as_view(), name='register'),
    url(r'^login/$', UserLoginAPIView.as_view(), name='login'),
    url(r'^logout/$', UserLogoutAPIView.as_view(), name='logout'),
    url(r'^details/$', UserDetailsAPIView.as_view(), name='details'),
    url(r'^list/$', UserListAPIView.as_view(), name='list'),
    # url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #     TemplateView.as_view(template_name='password_reset_confirm.html'),  name='password_reset_confirm'),
    # url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', PasswordResetConfirmView, name='password_reset_confirm'),
    url(r'^changepassword/', PasswordChangeView.as_view(), name='changepassword'),


    #
    # url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #         auth_views.password_reset_confirm, name='password_reset_confirm'),
    # url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    # # url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    # url(r'^password/reset/complete/$', auth_views.password_reset_complete,{'template_name': 'registeration/password_reset_complete.html'}, name='password_reset_complete')
]
