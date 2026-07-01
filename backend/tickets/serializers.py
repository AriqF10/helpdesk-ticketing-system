from rest_framework import serializers

from accounts.serializers import TechnicianSerializer, UserSerializer
from .models import Ticket, TicketAttachment, TicketComment


class TicketAttachmentSerializer(serializers.ModelSerializer):
    uploaded_by = UserSerializer(read_only=True)

    class Meta:
        model = TicketAttachment
        fields = ['id', 'file', 'uploaded_by', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_by', 'uploaded_at']


class TicketCommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = TicketComment
        fields = ['id', 'ticket', 'author', 'message', 'is_internal_note', 'created_at']
        read_only_fields = ['id', 'ticket', 'author', 'created_at']


class TicketListSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    assigned_to = TechnicianSerializer(read_only=True)
    response_sla_breached = serializers.ReadOnlyField()
    resolution_sla_breached = serializers.ReadOnlyField()

    class Meta:
        model = Ticket
        fields = [
            'id', 'title', 'status', 'priority', 'category',
            'created_by', 'assigned_to', 'created_at', 'updated_at',
            'response_due_at', 'resolution_due_at',
            'response_sla_breached', 'resolution_sla_breached',
        ]


class TicketDetailSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    assigned_to = TechnicianSerializer(read_only=True)
    comments = TicketCommentSerializer(many=True, read_only=True)
    attachments = TicketAttachmentSerializer(many=True, read_only=True)
    response_sla_breached = serializers.ReadOnlyField()
    resolution_sla_breached = serializers.ReadOnlyField()

    class Meta:
        model = Ticket
        fields = [
            'id', 'title', 'description', 'status', 'priority', 'category',
            'created_by', 'assigned_to', 'created_at', 'updated_at',
            'response_due_at', 'resolution_due_at',
            'first_response_at', 'resolved_at', 'closed_at',
            'response_sla_breached', 'resolution_sla_breached',
            'comments', 'attachments',
        ]
        read_only_fields = [
            'id', 'created_by', 'created_at', 'updated_at',
            'response_due_at', 'resolution_due_at',
            'first_response_at', 'resolved_at', 'closed_at',
        ]


class TicketCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'title', 'description', 'priority', 'category']


class TicketUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'status', 'priority', 'category', 'assigned_to']
