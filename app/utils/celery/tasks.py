from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from loguru import logger

import smtplib

from app.settings import settings

from app.utils.celery.celery_controller import celery_controller


@celery_controller.task(name="send_email")
def send_email(
    receiver_email: str,
    subject: str,
    body: str,
    sender_email: str = settings.MAIL_ADDRESS,
) -> bool:
    """
    Send a message by email.

    :return: message sending status.
    """

    # Create a message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    # Attaching text to the message
    message.attach(payload=MIMEText(body, "plain"))

    try:
        # Connecting to the SMTP server
        with smtplib.SMTP_SSL(
            host=settings.MAIL_SMTP_SERVER,
            port=settings.MAIL_SMTP_PORT,
        ) as server:
            server.login(
                user=settings.MAIL_ADDRESS,
                password=settings.MAIL_PASSWORD.get_secret_value(),
            )
            server.send_message(msg=message)

            logger.info("Email sent successfully!")

    except smtplib.SMTPConnectError:
        logger.error("Failed to connect to the email sending resource.")
        return False

    except smtplib.SMTPAuthenticationError:
        logger.error("The sender of the emails failed to authenticate.")
        return False

    except smtplib.SMTPException:
        logger.error("Error in working with the email sending resource.")
        return False

    return True
