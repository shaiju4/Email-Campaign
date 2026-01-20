import json
import logging

from django_celery_beat.models import ClockedSchedule, PeriodicTask

from campaigns.models import Campaign

logger = logging.getLogger(__name__)

def schedule_campaign(campaign:Campaign):
    """
    Schedule a one-off Celery task for the given campaign.
    """
    try:
        clocked, _ = ClockedSchedule.objects.get_or_create(
            clocked_time=campaign.scheduled_time
        )

        PeriodicTask.objects.create(
            clocked=clocked,
            one_off=True,
            name=f"Campaign-{campaign.id}",
            task="campaigns.tasks.execute_campaign",
            args=json.dumps([campaign.id]),
        )

    except Exception:
        logger.exception(
            "Unexpected error while scheduling campaign | campaign_id=%s",
            campaign.id,
        )
        raise
