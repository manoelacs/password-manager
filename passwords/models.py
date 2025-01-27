from django.contrib.auth.models import User
from django.db import models
from passwords.utils import password_generator


class PasswordEntry(models.Model):
    """Password Entry"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True, blank=True)
    icon = models.TextField(max_length=255, null=True, blank=True)
    notes = models.TextField(max_length=255, null=True, blank=True)
    url = models.URLField(blank=True, null=True)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    def set_random_password(self):
        """set a random password for field password"""
        self.password = password_generator()

    def __str__(self):
        return f"{self.url} ({self.user.username})"