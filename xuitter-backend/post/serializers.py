from rest_framework import serializers

from post.models import Action, Post, PostAction

class PostSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = Post
        fields = ['id', 'user', 'text', 'origin', 'created_at']
        read_only_fields = ['id', 'created_at']

class PostActionSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    action = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Action.objects.all()
    )
    
    class Meta:
        model = PostAction
        fields = ['id', 'user', 'post', 'action', 'created_at']
        read_only_fields = ['id', 'created_at']