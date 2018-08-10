from django.conf.urls import url
from .views import (PostCreateAPIView, PostListAPIView, PostDetailAPIView, PostDestroyAPIView, PostUpdateAPIView)


urlpatterns = [
    url(r'^$', PostListAPIView.as_view(), name='list'),
    url(r'^create/$', PostCreateAPIView.as_view(), name='create'),
    url(r'^(?P<slug>[\w-]+)/$', PostDetailAPIView.as_view(), name='detail'),
    url(r'^(?P<slug>[\w-]+)/edit/$', PostUpdateAPIView.as_view(), name='edit'),
    url(r'^(?P<slug>[\w-]+)/delete/$', PostDestroyAPIView.as_view(), name='destroy'),
]
