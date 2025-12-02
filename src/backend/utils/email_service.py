"""Email service for sending observation confirmation emails."""

import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib

from backend.configs.config import settings
from backend.models.observation import Observation
from backend.models.user import User

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
        message["From"] = settings.smtp_sender_email
        message["To"] = user.email

        # Create email body
        text_body = _create_text_email_body(observation, user)
        html_body = _create_html_email_body(observation, user)

        # Attach both plain text and HTML versions
        text_part = MIMEText(text_body, "plain")
        html_part = MIMEText(html_body, "html")
        message.attach(text_part)
        message.attach(html_part)

        # Send email
        await aiosmtplib.send(
            message,
            hostname=settings.smtp_server,
            port=settings.smtp_port,
            username=settings.smtp_username,
            password=settings.smtp_password,
            use_tls=settings.smtp_use_tls,
            start_tls=settings.smtp_start_tls,
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


def _create_text_email_body(observation: Observation, user: User) -> str:
    """Create plain text email body."""
    return f"""
Dear {user.username},

Your observation request has been successfully submitted!

Observation Details:
-------------------
Observation ID: {observation.observation_id}
Target Name: {observation.target_name}
Object: {observation.observation_object}
Coordinates: RA {observation.ra}°, Dec {observation.dec}°
Center Frequency: {observation.center_frequency} MHz
Integration Time: {observation.integration_time} seconds
Observation Type: {observation.observation_type}
Status: {observation.status}
Submitted At: {observation.submitted_at.strftime("%Y-%m-%d %H:%M:%S UTC")}

Your observation has been queued for processing. You will receive updates as the observation progresses.

Thank you for using Astro BEAM!

Best regards,
The Astro BEAM Team
"""


def _create_html_email_body(observation: Observation, user: User) -> str:
    """Create HTML email body."""
    return f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            background-color: #4a90e2;
            color: white;
            padding: 20px;
            text-align: center;
            border-radius: 5px 5px 0 0;
        }}
        .content {{
            background-color: #f9f9f9;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 0 0 5px 5px;
        }}
        .details {{
            background-color: white;
            padding: 15px;
            margin: 15px 0;
            border-left: 4px solid #4a90e2;
        }}
        .detail-row {{
            margin: 8px 0;
        }}
        .label {{
            font-weight: bold;
            color: #4a90e2;
        }}
        .footer {{
            text-align: center;
            margin-top: 20px;
            color: #777;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Observation Request Confirmed</h1>
        </div>
        <div class="content">
            <p>Dear {user.username},</p>
            <p>Your observation request has been successfully submitted!</p>

            <div class="details">
                <h3>Observation Details</h3>
                <div class="detail-row">
                    <span class="label">Observation ID:</span> {observation.observation_id}
                </div>
                <div class="detail-row">
                    <span class="label">Target Name:</span> {observation.target_name}
                </div>
                <div class="detail-row">
                    <span class="label">Object:</span> {observation.observation_object}
                </div>
                <div class="detail-row">
                    <span class="label">Coordinates:</span> RA {observation.ra}°, Dec {observation.dec}°
                </div>
                <div class="detail-row">
                    <span class="label">Center Frequency:</span> {observation.center_frequency} MHz
                </div>
                <div class="detail-row">
                    <span class="label">Integration Time:</span> {observation.integration_time} seconds
                </div>
                <div class="detail-row">
                    <span class="label">Observation Type:</span> {observation.observation_type}
                </div>
                <div class="detail-row">
                    <span class="label">Status:</span> <strong>{observation.status}</strong>
                </div>
                <div class="detail-row">
                    <span class="label">Submitted At:</span> {observation.submitted_at.strftime("%Y-%m-%d %H:%M:%S UTC")}
                </div>
            </div>

            <p>Your observation has been queued for processing. You will receive updates as the observation progresses.</p>

            <p>Thank you for using Astro BEAM!</p>

            <p>Best regards,<br>The Astro BEAM Team</p>
        </div>
        <div class="footer">
            <p>This is an automated message. Please do not reply to this email.</p>
        </div>
    </div>
</body>
</html>
"""
