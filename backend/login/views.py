from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, LoginLog
from django_user_agents.utils import get_user_agent
from .permissions import IsStudent, IsTeacher


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        role = request.data.get("role")

        if User.objects.filter(username=username).exists():
            return Response({"success": False, "message": "Username already exists"}, status=400)
        
        user = User.objects.create(
            username=username,
            password=make_password(password),
            role=role
        )
        return Response({"success": True, "message": f"{role.capitalize()} created successfully"})


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"success": False, "message": "Invalid username or password"}, status=401)
        
        if not check_password(password, user.password):
            return Response({"success": False, "message": "Invalid username or password"}, status=401)
        
        # Generate JWT token
        refresh = RefreshToken.for_user(user)

        # Log login details
        ip = request.META.get("REMOTE_ADDR")
        user_agent = get_user_agent(request)
        LoginLog.objects.create(
            user=user,
            ip_address=ip,
            user_agent=str(user_agent),
            device=user_agent.device.family,
            browser=user_agent.browser.family
        )

        return Response({
            "success": True,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "username": user.username,
            "role": user.role
        })


# 🔹 Role-based Views

class StudentDashboard(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def get(self, request):
        return Response({"message": f"Welcome Student {request.user.username}!"})

class TeacherDashboard(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    def get(self, request):
        return Response({"message": f"Welcome Teacher {request.user.username}!"})
