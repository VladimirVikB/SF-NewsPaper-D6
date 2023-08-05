from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import PostCategory
from newsapp.tasks import new_post_subscription


@receiver(m2m_changed, sender=PostCategory)
def notify_subscribers(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        pass
        new_post_subscription(instance)