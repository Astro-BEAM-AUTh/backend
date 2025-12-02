"""Email service for sending observation confirmation emails."""

import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib

from backend.configs.config import settings
from backend.models.observation import Observation
from backend.models.user import User
from backend.utils.email.templates.html import create_html_email_body_for_completion, create_html_email_body_for_confirmation
from backend.utils.email.templates.text import create_text_email_body_for_completion, create_text_email_body_for_confirmation

logger = logging.getLogger("astro_backend")


async def send_observation_confirmation_email(observation: Observation, user: User) -> None:
    """
    Send an email confirmation to the user after successful observation submission.

    Args:
        observation: The submitted observation
        user: The user who submitted the observation

    Raises:
        Exception: If email sending fails
    """
    try:
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = f"Observation Request Confirmed: {observation.observation_id}"
        message["To"] = user.email

        # Create email body
        text_body = create_text_email_body_for_confirmation(observation, user)
        html_body = create_html_email_body_for_confirmation(observation, user)

        # Send email
        await _send_email(
            message=message,
            text_body=MIMEText(text_body, "plain"),
            html_body=MIMEText(html_body, "html"),
        )

        logger.info(
            "Sent confirmation email to %s for observation %s",
            user.email,
            observation.observation_id,
        )
    except Exception:
        logger.exception(
            "Failed to send confirmation email to %s for observation %s",
            user.email,
            observation.observation_id,
        )
        # Don't raise - we don't want email failures to fail the observation submission
        # The observation is already saved, so we just log the error


async def send_observation_completion_email(observation: Observation, user: User) -> None:
    """
    Send an email notification to the user when their observation is completed.

    Args:
        observation: The completed observation
        user: The user who submitted the observation

    Raises:
        Exception: If email sending fails
    """
    try:
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = f"Observation Completed: {observation.observation_id}"
        message["To"] = user.email

        # Create email body
        text_body = create_text_email_body_for_completion(observation, user)
        html_body = create_html_email_body_for_completion(observation, user)

        # Send email
        await _send_email(
            message=message,
            text_body=MIMEText(text_body, "plain"),
            html_body=MIMEText(html_body, "html"),
        )

        logger.info(
            "Sent completion email to %s for observation %s",
            user.email,
            observation.observation_id,
        )
    except Exception:
        logger.exception(
            "Failed to send completion email to %s for observation %s",
            user.email,
            observation.observation_id,
        )
        # Don't raise - we don't want email failures to fail the observation update


async def _send_email(message: MIMEMultipart, text_body: MIMEText, html_body: MIMEText) -> None:
    """
    Send an email using aiosmtplib.

    Args:
        message (MIMEMultipart): The email message to send
        text_body (MIMEText): The plain text body of the email
        html_body (MIMEText): The HTML body of the email
    """
    message["From"] = settings.smtp_sender_email

    message.attach(text_body) if text_body else None
    message.attach(html_body) if html_body else None

    await aiosmtplib.send(
        message,
        hostname=settings.smtp_server,
        port=settings.smtp_port,
        username=settings.smtp_username,
        password=settings.smtp_password,
        use_tls=settings.smtp_use_tls,
        start_tls=settings.smtp_start_tls,
    )
