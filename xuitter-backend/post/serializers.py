from rest_framework import serializers

from post.models import Action, Post, PostAction


class PostSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    likes = serializers.SerializerMethodField()
    retweets = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()
    isLiked = serializers.SerializerMethodField()
    isReposted = serializers.SerializerMethodField()
    isCommented = serializers.SerializerMethodField()

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
            "isLiked",
            "isReposted",
            "isCommented",
        ]
        read_only_fields = ["id", "created_at"]

    def get_likes(self, obj):
        return PostAction.objects.filter(post=obj, action__slug="like").count()

    def get_retweets(self, obj):
        return PostAction.objects.filter(post=obj, action__slug="repost").count()

    def get_replies(self, obj):
        return PostAction.objects.filter(post=obj, action__slug="comment").count()

    def get_isLiked(self, obj):
        user = self.context.get("request").user
        if user.is_authenticated:
            return PostAction.objects.filter(
                post=obj, user=user, action__slug="like"
            ).exists()
        return False

    def get_isReposted(self, obj):
        user = self.context.get("request").user
        if user.is_authenticated:
            return PostAction.objects.filter(
                post=obj, user=user, action__slug="repost"
            ).exists()
        return False

    def get_isCommented(self, obj):
        user = self.context.get("request").user
        if user.is_authenticated:
            return PostAction.objects.filter(
                post=obj, user=user, action__slug="comment"
            ).exists()
        return False


class PostActionSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    action = serializers.SlugRelatedField(
        slug_field="slug", queryset=Action.objects.all()
    )

    class Meta:
        model = PostAction
        fields = ["id", "user", "post", "action", "created_at"]
        read_only_fields = ["id", "created_at"]
