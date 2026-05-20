from django import template

from homepage.models_site import ContactMessage

register = template.Library()


@register.simple_tag
def unread_contact_messages_count():
    return ContactMessage.objects.filter(is_read=False).count()
