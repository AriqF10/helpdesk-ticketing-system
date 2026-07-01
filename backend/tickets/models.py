from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import timedelta


class Ticket(models.Model):
    class Status(models.TextChoices):
        OPEN = 'open', 'Open'
        IN_PROGRESS = 'in_progress', 'In Progress'
        RESOLVED = 'resolved', 'Resolved'
        CLOSED = 'closed', 'Closed'

    class Priority(models.TextChoices):
        LOW = 'low', 'Low'
        MEDIUM = 'medium', 'Medium'
        HIGH = 'high', 'High'
        URGENT = 'urgent', 'Urgent'

    # SLA target in hours, keyed by priority
    SLA_RESPONSE_HOURS = {'low': 24, 'medium': 8, 'high': 4, 'urgent': 1}
    SLA_RESOLUTION_HOURS = {'low': 72, 'medium': 48, 'high': 24, 'urgent': 8}

    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    priority = models.CharField(max_length=20, choices=Priority.choices, default=Priority.MEDIUM)
    category = models.CharField(max_length=100, blank=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tickets_created'
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='tickets_assigned'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # SLA tracking
    response_due_at = models.DateTimeField(null=True, blank=True)
    resolution_due_at = models.DateTimeField(null=True, blank=True)
    first_response_at = models.DateTimeField(null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'#{self.id} {self.title}'

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        if is_new and not self.response_due_at:
            now = timezone.now()
            self.response_due_at = now + timedelta(hours=self.SLA_RESPONSE_HOURS[self.priority])
            self.resolution_due_at = now + timedelta(hours=self.SLA_RESOLUTION_HOURS[self.priority])
        super().save(*args, **kwargs)

    @property
    def response_sla_breached(self):
        if self.first_response_at:
            return self.first_response_at > self.response_due_at
        return timezone.now() > self.response_due_at if self.response_due_at else False

    @property
    def resolution_sla_breached(self):
        if self.resolved_at:
            return self.resolved_at > self.resolution_due_at
        return timezone.now() > self.resolution_due_at if self.resolution_due_at else False


class TicketComment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    is_internal_note = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comment by {self.author} on #{self.ticket_id}'


class TicketAttachment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='ticket_attachments/%Y/%m/')
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
