from rest_framework import permissions, viewsets

from accounts.permissions import IsAdminOrTechnician
from .models import Article
from .serializers import ArticleSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        qs = Article.objects.select_related('author')
        user = self.request.user
        if not (user.is_authenticated and (user.is_admin or user.is_technician)):
            qs = qs.filter(is_published=True)
        category = self.request.query_params.get('category')
        search = self.request.query_params.get('search')
        if category:
            qs = qs.filter(category=category)
        if search:
            qs = qs.filter(title__icontains=search)
        return qs

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [permissions.IsAuthenticated()]
        return [IsAdminOrTechnician()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
