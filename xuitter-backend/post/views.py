from django.db import models
from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.views import APIView

from post.models import Action, Post, PostAction
from post.serializers import PostSerializer, PostActionSerializer
from user.models import Contact


class PostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = PostSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save(user=request.user)

            origin_id = request.data.get("origin")
            if origin_id:
                PostAction.objects.create(
                    user=request.user,
                    post_id=origin_id,
                    action=Action.objects.get(slug="comment"),
                )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        if post.user != request.user:
            return Response(
                {"detail": "You do not have permission to delete this post."},
                status=status.HTTP_403_FORBIDDEN,
            )

        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostActionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        counts = (
            PostAction.objects.filter(post=post)
            .values("action__slug")
            .annotate(count=models.Count("id"))
        )
        response = {action["action__slug"]: action["count"] for action in counts}
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request, pk):
        data = request.data.copy()
        data["post"] = pk
        action_slug = data.get("action")
        user = request.user
        post = get_object_or_404(Post, pk=pk)

        if action_slug != "comment":
            existing = PostAction.objects.filter(
                user=user, post_id=pk, action__slug=action_slug
            )
            if existing.exists():
                existing.delete()
                return Response({"detail": f"{action_slug} removed."}, status=status.HTTP_204_NO_CONTENT)
            elif action_slug == "respost":
                repost_text = f"Reposted from {user.username}: {post.text}"
                Post.objects.create(
                    user=user,
                    origin=post,
                    text=repost_text
                )

        serializer = PostActionSerializer(data=data, context={"request": request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class FeedView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        feed_posts = Post.objects.filter(origin__isnull=True).order_by("-created_at")
        serializer = PostSerializer(feed_posts, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
