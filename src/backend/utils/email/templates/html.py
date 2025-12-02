import html

from backend.models.observation import Observation
from backend.models.user import User


def create_html_email_body_for_confirmation(observation: Observation, user: User) -> str:
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
            <p>Dear {html.escape(user.username)},</p>
            <p>Your observation request has been successfully submitted!</p>

            <div class="details">
                <h3>Observation Details</h3>
                <div class="detail-row">
                    <span class="label">Observation ID:</span> {html.escape(str(observation.observation_id))}
                </div>
                <div class="detail-row">
                    <span class="label">Target Name:</span> {html.escape(observation.target_name)}
                </div>
                <div class="detail-row">
                    <span class="label">Object:</span> {html.escape(observation.observation_object)}
                </div>
                <div class="detail-row">
                    <span class="label">Coordinates:</span> RA {html.escape(str(observation.ra))}°, Dec {html.escape(str(observation.dec))}°
                </div>
                <div class="detail-row">
                    <span class="label">Center Frequency:</span> {html.escape(str(observation.center_frequency))} MHz
                </div>
                <div class="detail-row">
                    <span class="label">Integration Time:</span> {html.escape(str(observation.integration_time))} seconds
                </div>
                <div class="detail-row">
                    <span class="label">Observation Type:</span> {html.escape(observation.observation_type)}
                </div>
                <div class="detail-row">
                    <span class="label">Status:</span> <strong>{html.escape(observation.status)}</strong>
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


def create_html_email_body_for_completion(observation: Observation, user: User) -> str:
    """Create HTML email body for observation completion."""
    duration = (observation.completed_at - observation.submitted_at).total_seconds() / 3600 if observation.completed_at else 0

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
            background-color: #28a745;
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
            border-left: 4px solid #28a745;
        }}
        .detail-row {{
            margin: 8px 0;
        }}
        .label {{
            font-weight: bold;
            color: #28a745;
        }}
        .success-badge {{
            background-color: #28a745;
            color: white;
            padding: 4px 8px;
            border-radius: 3px;
            font-weight: bold;
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
            <h1>✓ Observation Completed</h1>
        </div>
        <div class="content">
            <p>Dear {html.escape(user.username)},</p>
            <p><strong>Great news!</strong> Your observation has been completed successfully!</p>

            <div class="details">
                <h3>Observation Details</h3>
                <div class="detail-row">
                    <span class="label">Observation ID:</span> {html.escape(str(observation.observation_id))}
                </div>
                <div class="detail-row">
                    <span class="label">Target Name:</span> {html.escape(observation.target_name)}
                </div>
                <div class="detail-row">
                    <span class="label">Object:</span> {html.escape(observation.observation_object)}
                </div>
                <div class="detail-row">
                    <span class="label">Coordinates:</span> RA {html.escape(str(observation.ra))}°, Dec {html.escape(str(observation.dec))}°
                </div>
                <div class="detail-row">
                    <span class="label">Center Frequency:</span> {html.escape(str(observation.center_frequency))} MHz
                </div>
                <div class="detail-row">
                    <span class="label">Integration Time:</span> {html.escape(str(observation.integration_time))} seconds
                </div>
                <div class="detail-row">
                    <span class="label">Observation Type:</span> {html.escape(observation.observation_type)}
                </div>
                <div class="detail-row">
                    <span class="label">Output File:</span> <code>{html.escape(observation.output_filename)}</code>
                </div>
                <div class="detail-row">
                    <span class="label">Status:</span> <span class="success-badge">{html.escape(observation.status)}</span>
                </div>
                <div class="detail-row">
                    <span class="label">Submitted At:</span> {observation.submitted_at.strftime("%Y-%m-%d %H:%M:%S UTC")}
                </div>
                <div class="detail-row">
                    <span class="label">Completed At:</span> {observation.completed_at.strftime("%Y-%m-%d %H:%M:%S UTC") if observation.completed_at else "N/A"}
                </div>
                <div class="detail-row">
                    <span class="label">Processing Duration:</span> {html.escape(f"{duration:.2f}")} hours
                </div>
            </div>

            <p>Your observation data is now ready for analysis. You can access the results using the output filename provided above.</p>

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
