import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from campaigns.models import Campaign
from campaigns.services import schedule_campaign

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Campaign)
def campaign_schedule_handler(sender, instance, created, **kwargs):
    """
    Schedule campaign when status transitions to SCHEDULED.
    """
    if instance.status != Campaign.Status.SCHEDULED:
        return

    try:
        schedule_campaign(instance)

    except Exception:
        logger.exception(
            "Failed to schedule campaign | campaign_id=%s status=%s",
            instance.id,
            instance.status,
        )
