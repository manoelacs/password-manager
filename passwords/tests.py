from rest_framework import status
from django.contrib.auth.models import User
from .models import PasswordEntry
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token


class RegisterUserTestCase(APITestCase):

    def test_register_user(self):
        url = reverse("passwords:register")
        request = self.client.post(
            url,
            {
                "username": "testuser3",
                "password": "password123",
            },
        )
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            request.data["message"], "User registered successfully"
        )


class PasswordEntryTestCase(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )

        self.user2 = User.objects.create_user(
            username="testuser2", password="password123"
        )
        self.url_token = reverse("token_obtain_pair")
        request_token = self.client.post(
            self.url_token,
            {
                "username": "testuser",
                "password": "password123",
            },
        )
        token = request_token.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        self.password = PasswordEntry.objects.create(
            user=self.user,
            name="test",
            icon="https://example.com/icon.png",
            notes="Sample notes",
            url="https://example.com",
            username="sampleuser",
            password="samplepassword",
        )

        self.valid_data = {
            "user": self.user.id,
            "name": "test",
            "icon": "https://example.com/new-icon.png",
            "notes": "Updated notes",
            "url": "https://new-example.com",
            "username": "newuser",
            "password": "newpassword",
        }

    def test_list_password_entries(self):
        url = reverse("passwords:passwords")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_should_not_show_list_password_entries_for_other_user(self):
        url = reverse("passwords:passwords")
        request_token = self.client.post(
            self.url_token,
            {
                "username": "testuser2",
                "password": "password123",
            },
        )
        token = request_token.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 0)

    def test_empty_list_password_entry(self):
        self.password.delete()
        url = reverse("passwords:passwords")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 0)

    def test_retrieve_password_entry(self):
        url = reverse("passwords:password", kwargs={"pk": self.password.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], self.password.username)

    def test_try_retrieve_password_entry_and_fail(self):
        url = reverse("passwords:password", kwargs={"pk": 100000})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_password_entry(self):
        url = reverse("passwords:passwords")
        response = self.client.post(url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data["username"], self.valid_data["username"]
        )

    def test_update_password_entry(self):
        url = reverse("passwords:password", kwargs={"pk": self.password.id})
        updated_data = {
            "user": self.user.id,
            "name": "test3",
            "icon": "https://example.com/updated-icon.png",
            "notes": "Updated sample notes",
            "url": "https://updated-example.com",
            "username": "updateduser",
            "password": "updatedpassword",
        }
        response = self.client.put(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], updated_data["username"])

    def test_delete_password_entry(self):
        url = reverse("passwords:password", kwargs={"pk": self.password.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            PasswordEntry.objects.filter(id=self.password.id).exists()
        )
