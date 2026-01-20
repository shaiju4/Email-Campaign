import logging
import pandas as pd
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from .models import Recipient

logger = logging.getLogger(__name__)


def bulk_upload_recipients(file, uploaded_by=None) -> int:
    """
    Read a CSV file and bulk insert valid recipients into the database.

    Args:
        file: Uploaded CSV file.
        uploaded_by: Optional user object for auditing.

    Returns:
        int: Number of successfully inserted recipients.
    """
    filename = getattr(file, 'name', '')
    try:
        if filename.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(file)
            logger.info("Excel file loaded successfully by %s", uploaded_by)
        else:
            df = pd.read_csv(file)
            logger.info("CSV file loaded successfully by %s", uploaded_by)
    except Exception as e:
        logger.exception("Failed to read file '%s'", filename)
        raise

    recipients = []
    skipped_rows = 0

    for idx, row in df.iterrows():
        email = row.get("email")

        if not email or pd.isna(email):
            logger.warning("Row %s skipped: email is missing", idx)
            skipped_rows += 1
            continue

        try:
            validate_email(email)
        except ValidationError:
            logger.warning("Row %s skipped: invalid email '%s'", idx, email)
            skipped_rows += 1
            continue

        recipients.append(
            Recipient(
                name=row.get("name", ""),
                email=email,
                is_subscribed=row.get("is_subscribed", True),
            )
        )

    try:
        Recipient.objects.bulk_create(recipients, ignore_conflicts=True)
        logger.info(
            "%s recipients uploaded successfully by %s (%s rows skipped)",
            len(recipients),
            uploaded_by,
            skipped_rows,
        )
    except Exception:
        logger.exception("Failed to bulk insert recipients")
        raise

    return len(recipients)
