from rest_framework import serializers

from post.models import Action, Post, PostAction


class PostSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    likes = serializers.SerializerMethodField()
    retweets = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "user",
            "text",
            "origin",
            "created_at",
            "likes",
            "retweets",
            "replies",
        ]
        read_only_fields = ["id", "created_at"]

    def get_likes(self, obj):
        return PostAction.objects.filter(post=obj, action__slug="like").count()

    def get_retweets(self, obj):
        return PostAction.objects.filter(post=obj, action__slug="repost").count()

    def get_replies(self, obj):
        return PostAction.objects.filter(post=obj, action__slug="comment").count()


class PostActionSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    action = serializers.SlugRelatedField(
        slug_field="slug", queryset=Action.objects.all()
    )

    class Meta:
        model = PostAction
        fields = ["id", "user", "post", "action", "created_at"]
        read_only_fields = ["id", "created_at"]
