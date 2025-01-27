from passwords.models import PasswordEntry
from rest_framework import serializers


class PasswordEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = PasswordEntry
        fields = "__all__"
