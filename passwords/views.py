from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from .models import PasswordEntry
from .serializers.passwords_serializer import PasswordEntrySerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


class PasswordEntryView(APIView):
    """
    View to list all passwords in system
    """

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        "Return a list of passwords"
        passwords = PasswordEntry.objects.filter(user=request.user)
        passwords_serializer = PasswordEntrySerializer(passwords, many=True)
        return Response(passwords_serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        "Create a password entry"
        password_serializer = PasswordEntrySerializer(data=request.data)
        if password_serializer.is_valid():
            password_serializer.save()
            return Response(
                password_serializer.data, status=status.HTTP_201_CREATED
            )
        return Response(
            password_serializer.errors, status=status.HTTP_401_BAD_REQUEST
        )


class PasswordEntryViewDetail(APIView):
    """View to get, update and delete a pajsswordo entry"""

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self, pk):
        try:
            return PasswordEntry.objects.get(pk=pk)
        except PasswordEntry.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        password = self.get_object(pk)
        password_serializer = PasswordEntrySerializer(password)
        return Response(password_serializer.data)

    def put(self, request, pk):
        password = self.get_object(pk)
        password_serializer = PasswordEntrySerializer(
            password, data=request.data
        )
        if password_serializer.is_valid():
            password_serializer.save()
            return Response(
                password_serializer.data, status=status.HTTP_200_OK
            )
        return Response(
            password_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        password = self.get_object(pk)
        password.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
