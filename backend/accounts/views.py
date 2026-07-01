from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .permissions import IsAdminOrTechnician
from .serializers import RegisterSerializer, TechnicianSerializer, UserSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class MeView(APIView):
    def get(self, request):
        return Response(UserSerializer(request.user).data)


class TechnicianListView(generics.ListAPIView):
    queryset = User.objects.filter(role=User.Role.TECHNICIAN)
    serializer_class = TechnicianSerializer
    permission_classes = [IsAdminOrTechnician]
