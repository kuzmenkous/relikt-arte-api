from email.message import EmailMessage

import aiosmtplib

from src.adapters.broker import broker
from src.constants.mailer import EmailType
from src.mailer.db import save_emails
from src.mailer.settings import settings
from src.mailer.smtp import smtp_client
from src.schemas.mailer import EmailSend


@broker.subscriber("emails")
async def process_emails(send_data: EmailSend) -> None:
    msg = EmailMessage()
    msg["From"] = settings.smtp.from_email
    msg["To"] = ", ".join(send_data.emails)
    msg["Subject"] = send_data.subject

    if send_data.type == EmailType.TEXT:
        msg.set_content(send_data.body)
    elif send_data.type == EmailType.HTML:
        msg.set_content(
            "This email contains HTML content. Please view in an "
            "HTML compatible client."
        )
        msg.add_alternative(send_data.body, subtype="html")

    try:
        response = await smtp_client.send_message(msg, timeout=10)
        status = f"{response[0]}: {response[1]}"
    except aiosmtplib.SMTPException as e:
        status = f"error: {e}"
    except Exception as e:  # noqa: BLE001
        status = f"error: {e}"
    finally:
        await save_emails(send_data, status=status)
