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
        serializer = PostSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            
            origin_id = request.data['origin']
            if origin_id:
                PostAction.objects.create(
                    user=request.user,
                    post_id=origin_id,
                    action=Action.objects.get(slug='comment')
                )
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        
        if post.user != request.user:
            return Response(
                {"detail": "You do not have permission to delete this post."}, 
                status=status.HTTP_403_FORBIDDEN
            )

        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PostActionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        counts = (
            PostAction.objects
            .filter(post=post)
            .values('action__slug')
            .annotate(count=models.Count('id'))
        )
        response = {action['action__slug']: action['count'] for action in counts} 
        return Response(response, status=status.HTTP_200_OK)
    
    def post(self, request, pk):
        data = request.data.copy()
        data['post'] = pk
        
        serializer = PostActionSerializer(data=data, context={'request':request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class FeedView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        followed_accounts = [
            contact.user2 for contact in 
            Contact.objects.filter(user1=request.user)
        ]
        feed_posts = Post.objects.filter(user__in=followed_accounts).order_by("-created_at")
        response = [{
            "post_id": post.id,
            "user_id": post.user.id, 
            "origin": post.origin, 
            "created_at": post.created_at, 
            "content": post.text
        } for post in feed_posts]
        return Response(response, status=status.HTTP_200_OK)
        