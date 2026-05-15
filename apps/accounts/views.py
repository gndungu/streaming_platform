import json
from django.conf import settings
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.shortcuts import render
from django.contrib.auth import login as auth_login
from django.contrib.sessions.models import Session
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

from apps.accounts.models import UserSession
User = get_user_model()



def login(request, user):
    # Delete all existing sessions for this user
    UserSession.objects.filter(user=user).delete()
    # Delete Django session records
    Session.objects.filter(
        session_key__in=UserSession.objects.filter(user=user).values('session_key')
    ).delete()
    
    # Perform normal login
    auth_login(request, user)


class RegisterView(View):

    def post(self, request):

        data = json.loads(request.body)

        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if not username or not password:
            return JsonResponse({"error": "Username and password required"}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already exists"}, status=400)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return JsonResponse({
            "message": "Account created successfully",
            "user": {
                "id": user.id,
                "username": user.username
            }
        })


class LoginViewjwt(View):

    def post(self, request):

        data = json.loads(request.body)

        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)

        if user is None:
            return JsonResponse(
                {"error": "Invalid credentials"},
                status=401
            )

        # 🔥 CREATE JWT TOKENS
        refresh = RefreshToken.for_user(user)

        return JsonResponse({
            "message": "Login successful",
            "user": {
                "id": user.id,
                "username": user.username,
            },
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        })


class LoginView(View):

    def post(self, request):

        data = json.loads(request.body)

        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)

        if user is None:
            return JsonResponse({"error": "Invalid credentials"}, status=401)

        login(request, user)  # Django session login

        return JsonResponse({
            "message": "Login successful",
            "user": {
                "id": user.id,
                "username": user.phone_number
            }
        })
    

class LogoutView(View):

    def post(self, request):
        logout(request)

        return JsonResponse({
            "message": "Logged out successfully"
        })