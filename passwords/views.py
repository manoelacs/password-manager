from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from .models import PasswordEntry
from .serializers.passwords_serializer import PasswordEntrySerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class RegisterView(APIView):
    """
    A view to create user
    """
    @swagger_auto_schema(
        operation_description="Endpoint to create a login",
        responses={
            201: "Created",
            400: "Bad Request",
        },
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(
                    type=openapi.TYPE_STRING, description="Field username"),
                'email': openapi.Schema(
                    type=openapi.TYPE_STRING, description="Field email"),
                'password': openapi.Schema(
                    type=openapi.TYPE_STRING, description="Field password"),
            },
            required=['username', 'password']
        )
    )
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)


class PasswordEntryView(APIView):
    """
    View to list all passwords in system
    """

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    @swagger_auto_schema(
        operation_description="Endpoint to get all password's entry.",
        responses={
            200: "Success",
            401: "Unauthorized",
        },
    )
    def get(self, request):
        "Return a list of passwords"
        passwords = PasswordEntry.objects.filter(user=request.user)
        passwords_serializer = PasswordEntrySerializer(passwords, many=True)
        return Response(passwords_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Endpoint to create a entry password",
        responses={
            201: "Created",
            400: "Bad Request",
            401: "Unauthorized",
        },
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user': openapi.Schema(
                    type=openapi.TYPE_STRING, description="id account"),
                'name': openapi.Schema(
                    type=openapi.TYPE_STRING, description="Name for search"),
                'icon': openapi.Schema(
                    type=openapi.TYPE_STRING, description="Icon svg"),
                'notes': openapi.Schema(
                    type=openapi.TYPE_STRING, description="Notes"),
                'url': openapi.Schema(
                    type=openapi.TYPE_STRING, description="Url"),
                'username': openapi.Schema(
                    type=openapi.TYPE_STRING, description="Email or user"),
                'password': openapi.Schema(
                    type=openapi.TYPE_STRING, description="Password"),
            },
            required=['user', 'username', 'password']
        )
    )
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
    @swagger_auto_schema(
        operation_description="Endpoint Operation Description",
        responses={
            200: "Success",
            404: "Not Found",
            401: "Unauthorized",
        },
    )
    def get(self, request, pk):
        password = self.get_object(pk)
        password_serializer = PasswordEntrySerializer(password)
        return Response(password_serializer.data)

    @swagger_auto_schema(
        operation_description="Endpoint to create a entry password",
        responses={
            200: "Success",
            400: "Bad Request",
            404: "Not Found",
            401: "Unauthorized",
        },
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user': openapi.Schema(
                    type=openapi.TYPE_STRING, description="id account"),
                'name': openapi.Schema(
                    type=openapi.TYPE_STRING, description="Name for search"),
                'icon': openapi.Schema(
                    type=openapi.TYPE_STRING, description="Icon svg"),
                'notes': openapi.Schema(
                    type=openapi.TYPE_STRING, description="Notes"),
                'url': openapi.Schema(
                    type=openapi.TYPE_STRING, description="Url"),
                'username': openapi.Schema(
                    type=openapi.TYPE_STRING, description="Email or user"),
                'password': openapi.Schema(
                    type=openapi.TYPE_STRING, description="Password"),
            },
            required=['user', 'username', 'password']
        )
    )
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

    @swagger_auto_schema(
        operation_description="Endpoint Operation for delete passwod's entry.",
        responses={
            204: "No content",
            404: "Not Found",
            401: "Unauthorized",
        },
    )
    def delete(self, request, pk):
        password = self.get_object(pk)
        password.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
