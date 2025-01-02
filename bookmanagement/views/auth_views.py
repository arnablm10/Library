# app_name/views/auth_views.py

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class CustomTokenObtainPairView(TokenObtainPairView):
    pass

class TokenRefreshView(TokenRefreshView):
    pass
