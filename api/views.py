from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

import django_filters.rest_framework

from rest_framework import filters
from rest_framework import permissions
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.viewsets import ModelViewSet


from .models import Follow, Group, Post
from .serializers import CommentSerializer, FollowSerializer,\
                         GroupSerializer, PostSerializer

User = get_user_model()


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class PostViewSet(ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly
                          & IsOwnerOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['group']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly
                          & IsOwnerOrReadOnly]
    serializer_class = CommentSerializer

    def perform_create(self, serializer, *args, **kwargs):
        id = self.kwargs.get('post')
        post = get_object_or_404(Post, pk=id)
        serializer.save(author=self.request.user, post=post)

    def get_queryset(self, *args, **kwargs):
        id = self.kwargs.get('post')
        post_obj = get_object_or_404(Post, pk=id)
        return post_obj.comments


class FollowViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = FollowSerializer
    queryset = Follow.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['=user__username', '=following__username']

    def perform_create(self, serializer, *args, **kwargs):
        serializer.save(user=self.request.user)

class GroupViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
