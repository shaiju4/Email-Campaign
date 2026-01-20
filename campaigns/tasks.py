import logging

from celery import shared_task
from django.core.mail import send_mail

from campaigns.models import Campaign, EmailLogs
from recipients.models import Recipient
from campaigns.utils import generate_campaign_report, send_campaign_report

logger = logging.getLogger(__name__)


@shared_task(
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_kwargs={"max_retries": 3},
)
def execute_campaign(campaign_id: int) -> None:
    """
    Execute an email campaign by sending emails to all subscribed recipients.

    Args:
        self: Celery task instance (provided when `bind=True`).
        campaign_id (int): Primary key of the campaign to execute.

    Returns:
        None
    """

    try:
        campaign = Campaign.objects.filter(id=campaign_id).first()
        if not campaign:
            logger.warning(
                "Campaign not found for execution | campaign_id=%s",
                campaign_id,
            )
            return

        recipients = Recipient.objects.filter(is_subscribed=True)

        campaign.status = Campaign.Status.IN_PROGRESS
        campaign.total_recipients = recipients.count()
        campaign.save(update_fields=["status", "total_recipients"])

        for recipient in recipients.iterator():
            try:
                send_mail(
                    subject=campaign.subject,
                    message=campaign.content,
                    from_email="noreply@company.com",
                    recipient_list=[recipient.email],
                    fail_silently=False,
                )

                EmailLogs.objects.create(
                    campaign=campaign,
                    recipient_email=recipient.email,
                    status="SENT",
                )
                campaign.sent_count += 1

            except Exception as e:
                EmailLogs.objects.create(
                    campaign=campaign,
                    recipient_email=recipient.email,
                    status="FAILED",
                    failure_reason=str(e),
                )
                campaign.failed_count += 1

        campaign.status = Campaign.Status.COMPLETED
        campaign.save(update_fields=["status", "sent_count", "failed_count"])

        csv_content = generate_campaign_report(campaign)
        send_campaign_report(campaign, csv_content)

    except Exception:
        logger.exception(
            "Unexpected error during campaign execution | campaign_id=%s",
            campaign_id,
        )
        raise  
