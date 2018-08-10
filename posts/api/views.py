#from django.db.models import Q
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView, RetrieveAPIView, DestroyAPIView, CreateAPIView
from rest_framework.permissions import (IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny)
from rest_framework.filters import SearchFilter, OrderingFilter
from posts.models import Post
from .serializers import PostDetailSerializer, PostCreateUpdateSerializer, PostListSerializer
from .permissions import IsOwnerOrReadOnly


class PostCreateAPIView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    lookup_field = 'slug'
    #permission_classes = [IsAuthenticated, IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostDestroyAPIView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = 'slug'


class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'


class PostListAPIView(ListAPIView):
    queryset = Post.objects.all()
    permission_classes = [AllowAny]
    serializer_class = PostListSerializer
    lookup_field = 'slug'
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'content', 'user__first_name']
    # def get_queryset(self, *args, **kwargs):
    #     queryset_list = Post.objects.all()
    #     query = self.request.GET.get("q")
    #     if query:
    #         queryset_list = queryset_list.filter(
    #             Q(title__icontains = query) |
    #             Q(content__icontains=query) |
    #             #Q(user__icontains=query) |
    #             Q(user__first_name__icontains=query) |
    #             Q(user__last_name__icontains=query)
    #         ).distinct()
    #     return queryset_list


class PostUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)