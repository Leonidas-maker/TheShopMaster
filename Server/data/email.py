from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel
from typing import Dict, Any
from pathlib import Path
import configparser


class EmailSchema(BaseModel):
    email: EmailStr
    body: Dict[str, Any]
    type: str


def init_mailer(mail_from_name: str, ssl: bool = False):
    configPath = Path(__file__).parent.parent.absolute() / "config.ini"
    email_template_path = Path(__file__).parent.parent / "data" / "email_templates"
    config = configparser.ConfigParser()
    config.read(configPath)

    conf = ConnectionConfig(
        MAIL_USERNAME=config["EMAIL"]["username"],
        MAIL_PASSWORD=config["EMAIL"]["password"],
        MAIL_PORT=int(config["EMAIL"]["port"]),
        MAIL_SERVER=config["EMAIL"]["host"],
        MAIL_FROM=config["EMAIL"]["username"],
        MAIL_FROM_NAME=mail_from_name,
        MAIL_STARTTLS=False,
        MAIL_SSL_TLS=True,
        USE_CREDENTIALS=True,
        VALIDATE_CERTS=False,
        TEMPLATE_FOLDER=email_template_path,
    )
    return FastMail(conf)


async def send_with_template(email: EmailSchema):
    email_template = ""
    email_subject = ""
    email_ssl = False

    if email.type in ["first-verify", "verify-locked", "forgot-password"]:
        email_ssl = True

    match email.type:
        case "verify-first":
            email_template = "mail_verify_first.html"
            email_subject = "Verify your email address"
        case "verify-locked":
            email_template = "mail_verify_locked.html"
            email_subject = "Verify your email address"
        case "temporarily-locked":
            email_template = "mail_temporary_locked.html"
            email_subject = "Account temporarily locked"
        case "permanently-locked":
            email_template = "mail_permanent_locked.html"
            email_subject = "Account permanently locked"
        case "forgot-password":
            email_template = "mail_forgot_password.html"
            email_subject = "Reset your password"
        case "activate-2fa":
            email_template = "mail_activate_2fa.html"
            email_subject = "2FA activated"
        case "deactivate-2fa":
            email_template = "mail_deactivate_2fa.html"
            email_subject = "2FA deactivated"

    message = MessageSchema(
        subject=email_subject,
        recipients=[email.email],
        template_body=email.body,
        subtype=MessageType.html,
    )

    fm = init_mailer("TheShopMaster-Service", email_ssl)
    await fm.send_message(message, template_name=email_template)