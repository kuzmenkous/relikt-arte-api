from typing import Annotated

from pydantic import EmailStr, Field
from pydantic_settings import BaseSettings


class SMTPSettings(BaseSettings):
    hostname: Annotated[str, Field(validation_alias="SMTP_HOST")]
    port: Annotated[int, Field(validation_alias="SMTP_PORT")]
    username: Annotated[str, Field(validation_alias="SMTP_USER")]
    password: Annotated[str, Field(validation_alias="SMTP_PASSWORD")]
    use_tls: Annotated[bool, Field(validation_alias="SMTP_USE_TLS")]
    start_tls: Annotated[bool, Field(validation_alias="SMTP_START_TLS")]
    from_email: Annotated[EmailStr, Field(validation_alias="SMTP_FROM_EMAIL")]


class Settings(BaseSettings):
    debug: bool
    mailer_data_path: str

    # SMTP settings
    smtp: SMTPSettings = Field(default_factory=SMTPSettings)


settings = Settings()
