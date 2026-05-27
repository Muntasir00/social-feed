from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Post,
    PostImage,
    PostLike,
    Comment,
    CommentLike,
    Reply,
    ReplyLike,
)


class UserMiniSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "full_name"]

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ["id", "image"]


class ReplySerializer(serializers.ModelSerializer):
    author = UserMiniSerializer(read_only=True)
    like_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.BooleanField(read_only=True)

    class Meta:
        model = Reply
        fields = [
            "id",
            "author",
            "text",
            "created_at",
            "like_count",
            "is_liked",
        ]


class CommentSerializer(serializers.ModelSerializer):
    author = UserMiniSerializer(read_only=True)
    replies = ReplySerializer(many=True, read_only=True)
    like_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.BooleanField(read_only=True)

    class Meta:
        model = Comment
        fields = [
            "id",
            "author",
            "text",
            "created_at",
            "like_count",
            "is_liked",
            "replies",
        ]


class PostSerializer(serializers.ModelSerializer):
    author = UserMiniSerializer(read_only=True)
    images = PostImageSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    like_count = serializers.IntegerField(read_only=True)
    comment_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.BooleanField(read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "text",
            "visibility",
            "images",
            "like_count",
            "comment_count",
            "is_liked",
            "comments",
            "created_at",
        ]


class PostCreateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(), required=False, write_only=True
    )

    class Meta:
        model = Post
        fields = ["id", "text", "visibility", "images"]

    def create(self, validated_data):
        images = validated_data.pop("images", [])
        request = self.context["request"]

        post = Post.objects.create(author=request.user, **validated_data)

        for image in images:
            PostImage.objects.create(post=post, image=image)

        return post


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "text"]


class ReplyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = ["id", "text"]
