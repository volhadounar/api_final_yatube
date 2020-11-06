from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

import django_filters.rest_framework

from rest_framework import filters
from rest_framework import permissions
from rest_framework import serializers
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
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['group']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = CommentSerializer

    def perform_create(self, serializer, *args, **kwargs):
        id = self.kwargs.get('post')
        post = get_object_or_404(Post, pk=id)
        serializer.save(author=self.request.user, post=post)

    def get_queryset(self, *args, **kwargs):
        id = self.kwargs.get('post')
        post_obj = get_object_or_404(Post, pk=id)
        return post_obj.comments


class FollowViewSet(ModelViewSet):
    serializer_class = FollowSerializer
    queryset = Follow.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['=user__username', '=following__username']
    http_method_names = [u'get', u'post']

    def perform_create(self, serializer, *args, **kwargs):
        following_name = self.request.data['following']
        following = get_object_or_404(User, username=following_name)
        if Follow.objects.filter(
                following=following, user=self.request.user).count() > 0:
            raise serializers.ValidationError("item already exists")
        serializer.save(following=following, user=self.request.user)


class GroupViewSet(ModelViewSet):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    http_method_names = [u'get', u'post']
