from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from user.serializer import ContactSerializer, SignupSerializer, LoginSerializer
from user.models import Contact

class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "message": "User created",
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "user": {
                        "username": user.username,
                        "email": user.email,
                    },
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response(
                {"detail": "Refresh token required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"detail": "Logout successful."}, status=status.HTTP_205_RESET_CONTENT
            )
        except Exception:
            return Response(
                {"detail": "Invalid or non-blacklistable token."},
                status=status.HTTP_400_BAD_REQUEST,
            )

class ContactView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_pk):
        contacts = Contact.objects.filter(user1__pk=user_pk)
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data)

    def post(self, request, user_pk):
        serializer = ContactSerializer(data=request.data, context={"request": request})

        if serializer.is_valid():
            try:
                contact = serializer.save()
                return Response(
                    ContactSerializer(contact).data, status=status.HTTP_201_CREATED
                )
            except ValidationError as e:
                return Response(
                    {"errors": e.messages}, status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_pk):
        contact = get_object_or_404(
            Contact, user1_id=request.user.id, user2=request.data["user2"]
        )
        contact.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)