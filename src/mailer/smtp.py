import aiosmtplib

from src.mailer.settings import settings

smtp_client = aiosmtplib.SMTP(
    **settings.smtp.model_dump(exclude={"from_email"})
)
