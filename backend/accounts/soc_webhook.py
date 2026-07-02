import logging

import requests
from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)


def _client_ip(request):
    forwarded = request.META.get('HTTP_X_FORWARDED_FOR', '')
    if forwarded:
        return forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '0.0.0.0')


def send_login_event(request, username, success):
    """Best-effort notification to the SOC Dashboard demo webhook.

    SAFETY: only ever fires for the designated test account
    (SOC_WEBHOOK_TEST_USERNAME). Real end-user login data is never sent
    anywhere by this function. Never raises — a webhook outage must not
    block login.
    """
    test_username = getattr(settings, 'SOC_WEBHOOK_TEST_USERNAME', '')
    if not test_username or username != test_username:
        return

    url = getattr(settings, 'SOC_WEBHOOK_URL', '')
    secret = getattr(settings, 'SOC_WEBHOOK_SECRET', '')
    if not url or not secret:
        return

    event_type = 'login_success' if success else 'login_failed'
    payload = {
        'timestamp': timezone.now().isoformat(),
        'source_ip': _client_ip(request),
        'username': username,
        'event_type': event_type,
        'host': 'helpdesk-ticketing',
        'raw_message': f'{"Successful" if success else "Failed"} login attempt for test account "{username}"',
    }

    try:
        requests.post(
            url,
            json={'record': payload},
            headers={'X-Webhook-Secret': secret},
            timeout=2,
        )
    except requests.RequestException:
        logger.warning('Failed to notify SOC Dashboard webhook', exc_info=True)
