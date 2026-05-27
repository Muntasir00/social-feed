from django.db.models import Count, Exists, OuterRef, Q
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    Post,
    PostLike,
    Comment,
    CommentLike,
    Reply,
    ReplyLike,
)
from .serializers import (
    PostSerializer,
    PostCreateSerializer,
    CommentCreateSerializer,
    ReplyCreateSerializer,
    UserMiniSerializer,
)


class PostListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return PostCreateSerializer
        return PostSerializer

    def get_queryset(self):
        user = self.request.user

        return (
            Post.objects.filter(
                Q(visibility="public") | Q(visibility="private", author=user)
            )
            .select_related("author")
            .prefetch_related(
                "images",
                "comments",
                "comments__author",
                "comments__replies",
                "comments__replies__author",
            )
            .annotate(
                like_count=Count("likes", distinct=True),
                comment_count=Count("comments", distinct=True),
                is_liked=Exists(
                    PostLike.objects.filter(post=OuterRef("pk"), user=user)
                ),
            )
            .order_by("-created_at")
        )


class TogglePostLikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        post = Post.objects.get(id=post_id)

        like, created = PostLike.objects.get_or_create(post=post, user=request.user)

        if not created:
            like.delete()
            return Response({"liked": False})

        return Response({"liked": True})


class PostLikedUsersView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserMiniSerializer

    def get_queryset(self):
        post_id = self.kwargs["post_id"]
        return UserMiniSerializer.Meta.model.objects.filter(post_likes__post_id=post_id)


class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        post_id = self.kwargs["post_id"]
        post = Post.objects.get(id=post_id)

        serializer.save(post=post, author=self.request.user)


class ToggleCommentLikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, comment_id):
        comment = Comment.objects.get(id=comment_id)

        like, created = CommentLike.objects.get_or_create(
            comment=comment, user=request.user
        )

        if not created:
            like.delete()
            return Response({"liked": False})

        return Response({"liked": True})


class CommentLikedUsersView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserMiniSerializer

    def get_queryset(self):
        comment_id = self.kwargs["comment_id"]
        return UserMiniSerializer.Meta.model.objects.filter(
            comment_likes__comment_id=comment_id
        )


class ReplyCreateView(generics.CreateAPIView):
    serializer_class = ReplyCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        comment_id = self.kwargs["comment_id"]
        comment = Comment.objects.get(id=comment_id)

        serializer.save(comment=comment, author=self.request.user)


class ToggleReplyLikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, reply_id):
        reply = Reply.objects.get(id=reply_id)

        like, created = ReplyLike.objects.get_or_create(reply=reply, user=request.user)

        if not created:
            like.delete()
            return Response({"liked": False})

        return Response({"liked": True})


class ReplyLikedUsersView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserMiniSerializer

    def get_queryset(self):
        reply_id = self.kwargs["reply_id"]
        return UserMiniSerializer.Meta.model.objects.filter(
            reply_likes__reply_id=reply_id
        )
