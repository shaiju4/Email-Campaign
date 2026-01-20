import csv
import io
import logging

from django.core.mail import EmailMessage
from django.conf import settings

from .models import EmailLogs,Campaign

logger = logging.getLogger(__name__)

def generate_campaign_report(campaign: Campaign) -> str:
    """
    Generate a CSV report for a completed email campaign.

    Args:
        campaign (Campaign): The campaign instance.

    Returns:
        str: CSV content as a string .
    """
    buffer = io.StringIO()
    writer = csv.writer(buffer)

    writer.writerow(["Recipient Email", "Status", "Failure Reason"])

    logs = EmailLogs.objects.filter(campaign=campaign)
    for log in logs:
        writer.writerow([
            log.recipient_email,
            log.status,
            log.failure_reason or ""
        ])

    buffer.seek(0)
    return buffer.getvalue()

def send_campaign_report(campaign: Campaign, csv_content: str) -> None:
    """
    Send the campaign completion report to the configured admin email.

    Args:
        campaign (Campaign): The campaign instance for which the
            report is being sent.
        csv_content (str): The CSV content.

    Returns:
        None
    """
    subject = f"Campaign Report: {campaign.name}"
    body = f"""
Campaign Name: {campaign.name}
Total Recipients: {campaign.total_recipients}
Sent: {campaign.sent_count}
Failed: {campaign.failed_count}
Status: COMPLETED
"""
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email="noreply@company.com",
        to=[settings.ADMIN_EMAIL],
    )

    email.attach(
        filename=f"campaign_{campaign.id}_report.csv",
        content=csv_content,
        mimetype="text/csv",
    )

    try:
        email.send()
        logger.info(f"Campaign report email sent for campaign {campaign.id}")
    except Exception as e:
        logger.error(f"Failed to send campaign report email for campaign {campaign.id}: {e}")