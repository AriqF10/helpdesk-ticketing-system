from django.utils import timezone
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from accounts.permissions import IsOwnerOrStaff
from .models import Ticket, TicketAttachment, TicketComment
from .serializers import (
    TicketAttachmentSerializer,
    TicketCommentSerializer,
    TicketCreateSerializer,
    TicketDetailSerializer,
    TicketListSerializer,
    TicketUpdateSerializer,
)


class TicketViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrStaff]

    def get_queryset(self):
        user = self.request.user
        qs = Ticket.objects.select_related('created_by', 'assigned_to')
        if user.is_admin:
            pass
        elif user.is_technician:
            pass
        else:
            qs = qs.filter(created_by=user)

        status_param = self.request.query_params.get('status')
        priority_param = self.request.query_params.get('priority')
        assigned_param = self.request.query_params.get('assigned_to')
        if status_param:
            qs = qs.filter(status=status_param)
        if priority_param:
            qs = qs.filter(priority=priority_param)
        if assigned_param:
            qs = qs.filter(assigned_to_id=assigned_param)
        return qs

    def get_serializer_class(self):
        if self.action == 'list':
            return TicketListSerializer
        if self.action == 'create':
            return TicketCreateSerializer
        if self.action in ('update', 'partial_update'):
            return TicketUpdateSerializer
        return TicketDetailSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        instance = serializer.instance
        new_status = serializer.validated_data.get('status', instance.status)
        extra = {}
        if new_status == Ticket.Status.RESOLVED and not instance.resolved_at:
            extra['resolved_at'] = timezone.now()
        if new_status == Ticket.Status.CLOSED and not instance.closed_at:
            extra['closed_at'] = timezone.now()
        serializer.save(**extra)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def dashboard(self, request):
        qs = self.get_queryset()
        by_status = {choice: qs.filter(status=choice).count() for choice, _ in Ticket.Status.choices}
        by_priority = {choice: qs.filter(priority=choice).count() for choice, _ in Ticket.Priority.choices}
        open_tickets = qs.exclude(status__in=[Ticket.Status.RESOLVED, Ticket.Status.CLOSED])
        sla_breached = sum(1 for t in open_tickets if t.resolution_sla_breached)
        return Response({
            'total': qs.count(),
            'by_status': by_status,
            'by_priority': by_priority,
            'sla_breached': sla_breached,
        })


class TicketCommentViewSet(viewsets.ModelViewSet):
    serializer_class = TicketCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = TicketComment.objects.filter(ticket_id=self.kwargs['ticket_pk']).select_related('author')
        user = self.request.user
        if not (user.is_admin or user.is_technician):
            qs = qs.exclude(is_internal_note=True)
        return qs

    def perform_create(self, serializer):
        ticket = Ticket.objects.get(pk=self.kwargs['ticket_pk'])
        comment = serializer.save(author=self.request.user, ticket=ticket)
        if (self.request.user.is_admin or self.request.user.is_technician) and not ticket.first_response_at:
            ticket.first_response_at = timezone.now()
            ticket.save(update_fields=['first_response_at'])
        return comment


class TicketAttachmentViewSet(viewsets.ModelViewSet):
    serializer_class = TicketAttachmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return TicketAttachment.objects.filter(ticket_id=self.kwargs['ticket_pk'])

    def perform_create(self, serializer):
        ticket = Ticket.objects.get(pk=self.kwargs['ticket_pk'])
        serializer.save(uploaded_by=self.request.user, ticket=ticket)
