from django.test import TestCase
from django.core.exceptions import ValidationError
from user.models import User
from post.models import Post, Action, PostAction


class PostModelsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@email.com", password="123456"
        )
        self.other_user = User.objects.create_user(
            username="otheruser", email="other@email.com", password="654321"
        )
        self.action_like = Action.objects.create(name="Like", slug="like")
        self.action_repost = Action.objects.create(name="Repost", slug="repost")
        self.post = Post.objects.create(user=self.user, text="Hello world!")
        self.reply = Post.objects.create(
            user=self.other_user, text="Reply!", origin=self.post
        )

    def test_post_str(self):
        self.assertIn(self.user.username, str(self.post))
        self.assertIn(str(self.post.created_at.date()), str(self.post))

    def test_post_reply_relationship(self):
        self.assertEqual(self.reply.origin, self.post)
        self.assertIn(self.reply, self.post.replies.all())

    def test_post_text_max_length(self):
        long_text = "a" * 301
        post = Post(user=self.user, text=long_text)
        with self.assertRaises(ValidationError):
            post.full_clean()

    def test_action_str(self):
        self.assertEqual(str(self.action_like), "Like")
        self.assertEqual(str(self.action_repost), "Repost")

    def test_action_slug_unique(self):
        with self.assertRaises(Exception):
            Action.objects.create(name="Duplicate Like", slug="like")

    def test_postaction_str(self):
        post_action = PostAction.objects.create(
            user=self.user, post=self.post, action=self.action_like
        )
        self.assertIn(self.user.username, str(post_action))
        self.assertIn(self.action_like.name, str(post_action))
