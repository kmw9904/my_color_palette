# community/serializers.py
from rest_framework import serializers
from .models import Post, Comment

class CommentSerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Comment
        fields = ['id', 'user', 'user_username', 'text', 'created_at']
        read_only_fields = ['user', 'created_at', 'user_username']

class PostSerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField(source='user.username')
    likes_count = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 'user', 'user_username', 'image', 'caption', 'tags',
            'created_at', 'likes_count', 'comments'
        ]
        read_only_fields = ['user', 'created_at', 'likes_count', 'comments', 'user_username']

    def get_likes_count(self, obj):
        return obj.likes.count()
