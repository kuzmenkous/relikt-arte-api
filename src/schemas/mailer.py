from pydantic import BaseModel, EmailStr

from src.constants.mailer import EmailType


class EmailSend(BaseModel):
    subject: str
    body: str
    type: EmailType
    emails: set[EmailStr]
