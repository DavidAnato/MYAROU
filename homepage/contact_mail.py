from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .models_site import SiteSettings, ContactMessage


REQUEST_TYPE_LABELS = dict(ContactMessage.REQUEST_TYPE_CHOICES)


def send_contact_notification(message: ContactMessage) -> bool:
    site = SiteSettings.get_solo()
    recipient = site.notify_email
    if not recipient:
        return False

    request_label = REQUEST_TYPE_LABELS.get(message.request_type, message.request_type or '—')
    subject = f"[MYAROU Contact] {message.subject}"
    body = render_to_string('email/contact_notification.txt', {
        'message': message,
        'request_label': request_label,
        'site': site,
    })

    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None) or 'noreply@myarou.com'
    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=from_email,
            recipient_list=[recipient],
            fail_silently=False,
        )
        return True
    except Exception:
        return False
