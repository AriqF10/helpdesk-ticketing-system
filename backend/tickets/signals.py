from django.core.mail import send_mail
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from accounts.models import User
from .models import Ticket


def _send(subject, message, recipient_list):
    recipient_list = [r for r in recipient_list if r]
    if not recipient_list:
        return
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list, fail_silently=True)


@receiver(pre_save, sender=Ticket)
def stash_old_ticket_state(sender, instance, **kwargs):
    if instance.pk:
        try:
            old = Ticket.objects.get(pk=instance.pk)
            instance._old_status = old.status
            instance._old_assigned_to_id = old.assigned_to_id
        except Ticket.DoesNotExist:
            instance._old_status = None
            instance._old_assigned_to_id = None
    else:
        instance._old_status = None
        instance._old_assigned_to_id = None


@receiver(post_save, sender=Ticket)
def notify_on_ticket_changes(sender, instance, created, **kwargs):
    if created:
        staff_emails = User.objects.filter(
            role__in=[User.Role.ADMIN, User.Role.TECHNICIAN]
        ).values_list('email', flat=True)
        _send(
            f'[Helpdesk] New ticket #{instance.id}: {instance.title}',
            f'A new ticket was created by {instance.created_by}.\n\n{instance.description}',
            list(staff_emails),
        )
        return

    old_status = getattr(instance, '_old_status', None)
    if old_status is not None and old_status != instance.status:
        _send(
            f'[Helpdesk] Ticket #{instance.id} status changed to {instance.get_status_display()}',
            f'Your ticket "{instance.title}" is now {instance.get_status_display()}.',
            [instance.created_by.email],
        )

    old_assigned_id = getattr(instance, '_old_assigned_to_id', None)
    if instance.assigned_to_id and old_assigned_id != instance.assigned_to_id:
        _send(
            f'[Helpdesk] Ticket #{instance.id} assigned to you',
            f'Ticket "{instance.title}" has been assigned to you.',
            [instance.assigned_to.email],
        )
