from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from .views import TicketAttachmentViewSet, TicketCommentViewSet, TicketViewSet

router = DefaultRouter()
router.register('tickets', TicketViewSet, basename='ticket')

tickets_router = routers.NestedDefaultRouter(router, 'tickets', lookup='ticket')
tickets_router.register('comments', TicketCommentViewSet, basename='ticket-comments')
tickets_router.register('attachments', TicketAttachmentViewSet, basename='ticket-attachments')

urlpatterns = router.urls + tickets_router.urls
