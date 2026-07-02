from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .permissions import IsAdminOrTechnician
from .serializers import RegisterSerializer, TechnicianSerializer, UserSerializer
from .soc_webhook import send_login_event


class ThrottledTokenObtainPairView(TokenObtainPairView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'auth'

    def post(self, request, *args, **kwargs):
        username = request.data.get('username', '')
        try:
            response = super().post(request, *args, **kwargs)
        except Exception:
            send_login_event(request, username, success=False)
            raise
        send_login_event(request, username, success=(response.status_code == 200))
        return response


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
