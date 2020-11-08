from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Comment, Follow, Group, Post


User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(many=False, read_only=True,
                                          slug_field='username')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date', 'group')
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(many=False, read_only=True,
                                          slug_field='username')

    class Meta:
        fields = ('id', 'author', 'post', 'text', 'created')
        model = Comment
        read_only_fields = ['post']


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
                    slug_field='username',
                    many=False, read_only=False,
                    default=serializers.CurrentUserDefault(),
                    queryset=User.objects.all())
    following = serializers.SlugRelatedField(
                    slug_field='username',
                    many=False,
                    read_only=False,
                    queryset=User.objects.all())

    def validate(self, data):
        following = data['following']
        user = data['user']
        if user == following:
            raise serializers.ValidationError(
                              "trying to subscribe to yourself")
        return data

    class Meta:
        fields = ('user', 'following')
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['following', 'user']
            )
        ]


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'title',)
        model = Group
