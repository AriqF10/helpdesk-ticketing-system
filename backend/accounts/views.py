from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .permissions import IsAdminOrTechnician
from .serializers import RegisterSerializer, TechnicianSerializer, UserSerializer


class ThrottledTokenObtainPairView(TokenObtainPairView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'auth'


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'auth'


class MeView(APIView):
    def get(self, request):
        return Response(UserSerializer(request.user).data)


class TechnicianListView(generics.ListAPIView):
    queryset = User.objects.filter(role=User.Role.TECHNICIAN)
    serializer_class = TechnicianSerializer
    permission_classes = [IsAdminOrTechnician]
