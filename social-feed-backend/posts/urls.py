from django.urls import path
from .views import (
    PostListCreateView,
    TogglePostLikeView,
    PostLikedUsersView,
    CommentCreateView,
    ToggleCommentLikeView,
    CommentLikedUsersView,
    ReplyCreateView,
    ToggleReplyLikeView,
    ReplyLikedUsersView,
)

urlpatterns = [
    path("posts/", PostListCreateView.as_view(), name="post-list-create"),
    path("posts/<int:post_id>/like/", TogglePostLikeView.as_view(), name="post-like"),
    path(
        "posts/<int:post_id>/likes/",
        PostLikedUsersView.as_view(),
        name="post-liked-users",
    ),
    path(
        "posts/<int:post_id>/comments/",
        CommentCreateView.as_view(),
        name="comment-create",
    ),
    path(
        "comments/<int:comment_id>/like/",
        ToggleCommentLikeView.as_view(),
        name="comment-like",
    ),
    path(
        "comments/<int:comment_id>/likes/",
        CommentLikedUsersView.as_view(),
        name="comment-liked-users",
    ),
    path(
        "comments/<int:comment_id>/replies/",
        ReplyCreateView.as_view(),
        name="reply-create",
    ),
    path(
        "replies/<int:reply_id>/like/", ToggleReplyLikeView.as_view(), name="reply-like"
    ),
    path(
        "replies/<int:reply_id>/likes/",
        ReplyLikedUsersView.as_view(),
        name="reply-liked-users",
    ),
]
