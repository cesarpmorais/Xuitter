import json

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

from django.test import TestCase, Client
from django.urls import reverse

from user.models import User
from post.models import Action, Post, PostAction


def authenticate(user):
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    auth_header = {
        'HTTP_AUTHORIZATION': f'Bearer {access_token}'
    }
    return auth_header
        
class PostTestCase(TestCase):
    fixtures = ['actions.json', 'users.json']
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(pk=1)
        self.post = Post.objects.create(user=self.user, text="This is a test post.")
    
    def test_create_post(self):
        valid_post_data = {
            "text": "This is a test post.",
            "origin": None
        }
        response = self.client.post(
            reverse('post'),
            json.dumps(valid_post_data),
            content_type='application/json',
            **authenticate(self.user)
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        post = Post.objects.get(pk=1)
        self.assertEqual(valid_post_data['text'], post.text)
        self.assertEqual(self.user, post.user)
    
    def test_invalid_post_exception(self):
        invalid_post_data = {
            "texto": "This is a test post.",
            "origin": None
        }
        response = self.client.post(
            reverse('post'),
            json.dumps(invalid_post_data),
            content_type='application/json',
            **authenticate(self.user)
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_delete_post(self):
        response = self.client.delete(
            reverse('post-detail', args=[self.post.pk]),
            **authenticate(self.user)
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())
    
    def test_delete_post_unauthorized_user(self):
        alt_user = User.objects.get(pk=2)
        response = self.client.delete(
            reverse('post-detail', args=[self.post.pk]),
            **authenticate(alt_user)
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Post.objects.filter(pk=self.post.pk).exists())
    
    def test_create_post_comment(self):
        valid_comment_data = {
            'origin': self.post.pk,
            'text': 'This is a test comment.'
        }
        response = self.client.post(
            reverse('post'),
            json.dumps(valid_comment_data),
            content_type='application/json',
            **authenticate(self.user)
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        comment = Post.objects.get(origin_id=valid_comment_data['origin'])
        self.assertEqual(comment.origin, self.post)
        self.assertEqual(comment.text, valid_comment_data['text'])
    

class PostActionTestCase(TestCase):
    fixtures = ['actions.json', 'users.json']
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(pk=1)
        self.like = {'action': 'like'}
        self.repost = {'action': 'repost'}
        self.post = Post.objects.create(user=self.user, text="This is a test post.")
        
    def test_create_post_like(self):
        response = self.client.post(
            reverse('post-action', args=[self.post.pk]),
            json.dumps(self.like),
            content_type='application/json',
            **authenticate(self.user)
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        post_action = PostAction.objects.get(post_id=self.post.pk)
        self.assertEqual(self.like['action'], post_action.action.slug)
        self.assertEqual(self.post, post_action.post)
        self.assertEqual(self.user, post_action.user)

    def test_create_post_repost(self):
        response = self.client.post(
            reverse('post-action', args=[self.post.pk]),
            json.dumps(self.repost),
            content_type='application/json',
            **authenticate(self.user)
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        post_action = PostAction.objects.get(post_id=self.post.pk)
        self.assertEqual(self.repost['action'], post_action.action.slug)
        self.assertEqual(self.post, post_action.post)
        self.assertEqual(self.user, post_action.user)

    def test_get_post_like_count(self):
        for i in range(1,5):
            PostAction.objects.create(
                post=self.post,
                user=User.objects.get(pk=i),
                action=Action.objects.get(slug='like')
            )
            
        response = self.client.get(
            reverse('post-action', args=[self.post.pk]),
            **authenticate(self.user)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = json.loads(response.content)
        self.assertEqual(data['like'], 4)

    def test_get_post_repost_count(self):
        for i in range(1,5):
            PostAction.objects.create(
                post=self.post,
                user=User.objects.get(pk=i),
                action=Action.objects.get(slug='repost')
            )
        
        response = self.client.get(
            reverse('post-action', args=[self.post.pk]),
            **authenticate(self.user)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = json.loads(response.content)
        self.assertEqual(data['repost'], 4)
    
    def test_get_post_comment_count(self):
        for i in range(1,5):
            valid_comment_data = {
                'origin': self.post.pk,
                'text': f'This is the {i} test comment.'
            }
            response = self.client.post(
                reverse('post'),
                json.dumps(valid_comment_data),
                content_type='application/json',
                **authenticate(self.user)
            )
        
        response = self.client.get(
            reverse('post-action', args=[self.post.pk]),
            **authenticate(self.user)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = json.loads(response.content)
        self.assertEqual(data['comment'], 4)
        
    def test_get_multiple_action_data(self):
        for i in range(1,5):
            PostAction.objects.create(
                post=self.post,
                user=User.objects.get(pk=i),
                action=Action.objects.get(slug='like')
            )
            PostAction.objects.create(
                post=self.post,
                user=User.objects.get(pk=i),
                action=Action.objects.get(slug='repost')
            )
            valid_comment_data = {
                'origin': self.post.pk,
                'text': f'This is the {i} test comment.'
            }
            response = self.client.post(
                reverse('post'),
                json.dumps(valid_comment_data),
                content_type='application/json',
                **authenticate(self.user)
            )
            
        response = self.client.get(
            reverse('post-action', args=[self.post.pk]),
            **authenticate(self.user)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = json.loads(response.content)
        self.assertEqual(data['like'], 4)
        self.assertEqual(data['repost'], 4)
        self.assertEqual(data['comment'], 4)

class FeedTestCase(TestCase):
    fixtures = ['users.json', 'contacts.json', 'posts.json']
    
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=4)
        
    def test_get_feed_posts(self):
        response = self.client.get(
            reverse('feed'),
            **authenticate(self.user1)
        )
        posts = json.loads(response.content)
        self.assertEquals(len(posts), 7)
        
        for post in posts:
            self.assertIn('post_id', post)
            self.assertIn('user_id', post)
            self.assertIn('origin', post)
            self.assertIn('created_at', post)
            self.assertIn('content', post)
    
    def test_get_feed_with_no_posts(self):
        response = self.client.get(
            reverse('feed'),
            **authenticate(self.user2)
        )
        posts = json.loads(response.content)
        self.assertEquals(len(posts), 0)