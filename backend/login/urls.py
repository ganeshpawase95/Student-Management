from django.contrib import admin
from django.urls import path
from login.views import RegisterView, LoginView, StudentDashboard, TeacherDashboard

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path("student/dashboard/", StudentDashboard.as_view(), name="student-dashboard"),
    path("teacher/dashboard/", TeacherDashboard.as_view(), name="teacher-dashboard"),
]