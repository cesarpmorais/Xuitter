import json
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient, APITestCase
from django.test import TestCase, Client
from django.urls import reverse

from user.models import Contact, User


class AuthTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        User.objects.create_user(
            username="TestUser", email="testuser@email.com", password="t3stp4assw0rd"
        )

    def test_valid_signup(self):
        valid_signup_data = {
            "username": "NewUser",
            "email": "newuser@email.com",
            "password": "T3stP4as5w0rd",
        }
        response = self.client.post(
            reverse("signup"),
            data=json.dumps(valid_signup_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_user = User.objects.get(username=valid_signup_data["username"])
        self.assertEqual(valid_signup_data["username"], created_user.username)
        self.assertEqual(valid_signup_data["email"], created_user.email)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_invalid_signup(self):
        invalid_signup_data = {
            "username": "NewUser",
            "email": "newuser@email.com",
            "password": "2Sh0rt",
        }
        response = self.client.post(
            reverse("signup"),
            data=json.dumps(invalid_signup_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("access", response.data)
        self.assertNotIn("refresh", response.data)

    def test_valid_login(self):
        valid_login_data = {
            "email": "testuser@email.com",
            "password": "t3stp4assw0rd",
        }
        response = self.client.post(
            reverse("login"),
            data=json.dumps(valid_login_data),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_invalid_creadentials_login(self):
        invalid_login_data = {
            "email": "testuser@email.com",
            "password": "wr0ngp4assw0rd",
        }
        response = self.client.post(
            reverse("login"),
            data=json.dumps(invalid_login_data),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn("access", response.data)
        self.assertNotIn("refresh", response.data)

    def test_non_existent_user_login(self):
        non_existent_user_data = {
            "email": "nonexistentuser@email.com",
            "password": "t3stp4assw0rd",
        }
        response = self.client.post(
            reverse("login"),
            data=json.dumps(non_existent_user_data),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn("access", response.data)
        self.assertNotIn("refresh", response.data)

    def test_logout_success(self):
        user = User.objects.get(email="testuser@email.com")
        refresh = str(RefreshToken.for_user(user))
        access = str(RefreshToken.for_user(user).access_token)
        response = self.client.post(
            reverse("logout"),
            data=json.dumps({"refresh": refresh}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {access}",
        )
        self.assertEqual(response.status_code, 205)
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], "Logout successful.")

    def test_logout_missing_token(self):
        user = User.objects.get(email="testuser@email.com")
        access = str(RefreshToken.for_user(user).access_token)
        response = self.client.post(
            reverse("logout"),
            data=json.dumps({}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {access}",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], "Refresh token required.")

    def test_logout_invalid_token(self):
        user = User.objects.get(email="testuser@email.com")
        access = str(RefreshToken.for_user(user).access_token)
        response = self.client.post(
            reverse("logout"),
            data=json.dumps({"refresh": "invalidtoken"}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {access}",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], "Invalid or non-blacklistable token.")

class ContactTestCase(APITestCase):
    fixtures = ["addresses.json", "users.json", "contacts.json"]

    def setUp(self):
        self.user = User.objects.get(pk=2)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_user_followed_contacts(self):
        response = self.client.get(
            reverse("user-contacts", args=[self.user.pk]), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_contacts = Contact.objects.filter(user1=self.user)
        self.assertEqual(len(user_contacts), len(response.data))

    def test_create_contact(self):
        contact_data = {"user2": 3}
        response = self.client.post(
            reverse("user-contacts", args=[self.user.pk]),
            data=contact_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        contact = Contact.objects.get(id=response.data["id"])
        self.assertEqual(contact.user1.pk, response.data["follower"])
        self.assertEqual(contact.user2.pk, response.data["followed"])

    def test_create_user_with_invalid_data(self):
        contact_data = {}
        response = self.client.post(
            reverse("user-contacts", args=[self.user.pk]),
            data=contact_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_same_user_contact(self):
        contact_data = {"user2": 2}
        response = self.client.post(
            reverse("user-contacts", args=[self.user.pk]),
            data=contact_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("errors", response.data)

    def test_delete_contact(self):
        delete_contact_data = {"user2": 1}
        response = self.client.delete(
            reverse("user-contacts", args=[self.user.pk]),
            data=delete_contact_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Contact.objects.filter(user1_id=self.user.id, user2_id=1).exists()
        )

    def test_delete_non_existing_contact(self):
        delete_contact_data = {"user2": 3}
        response = self.client.delete(
            reverse("user-contacts", args=[self.user.pk]),
            data=delete_contact_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)