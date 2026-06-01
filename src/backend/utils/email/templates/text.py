from email.mime.text import MIMEText

from backend.models.observation import Observation
from backend.models.user import User


def _create_observation_details_text(observation: Observation) -> str:
    """Create the observation details section of the email."""
    return f"""Observation Details:
-------------------
Observation ID: {observation.id}
Target Name: {observation.target_name}
Coordinates: RA {observation.ra}°, Dec {observation.dec}°
Bandwidth: {observation.bandwidth.value} MHz
Center Frequency: {observation.center_frequency.value} MHz
Velocity Reference Frame: {observation.velocity_frame.value}
Integration Time: {observation.integration_time} seconds
FFT Size: {observation.fft_size}
Observation Type: {observation.observation_type}
Planned Start: {observation.planned_start.strftime("%Y-%m-%d %H:%M:%S UTC") if observation.planned_start else "N/A"}
Status: {observation.status}
Created On: {observation.created_on.strftime("%Y-%m-%d %H:%M:%S UTC")}
{f"CSV Download URL: {observation.csv_download_url}" if observation.csv_download_url else ""}
{f"Data Download URL: {observation.data_download_url}" if observation.data_download_url else ""}
{f"Analysis Results URL: {observation.analysis_results_url}" if observation.analysis_results_url else ""}
""".strip()


def create_text_email_body_for_confirmation(observation: Observation, user: User) -> MIMEText:
    """Create plain text email body."""
    return MIMEText(
        f"""
Dear {user.username},

Your observation request has been successfully submitted!

{_create_observation_details_text(observation)}

Your observation has been queued for processing. You will receive updates as the observation progresses.

Thank you for using Astro BEAM!

Best regards,
The Astro BEAM Team
""",
        _subtype="plain",
    )


def create_text_email_body_for_completion(observation: Observation, user: User) -> MIMEText:
    """Create plain text email body for observation completion."""
    if observation.completed_on is None:
        msg = "Cannot create completion email for observation without completed_on timestamp"
        raise ValueError(msg)
    duration = (observation.completed_on - observation.created_on).total_seconds() / 3600 if observation.completed_on else 0

    return MIMEText(
        f"""
Dear {user.username},

Great news! Your observation has been completed successfully!

{_create_observation_details_text(observation)}

Processing Duration: {duration:.2f} hours

Your observation data is now ready for analysis. You can access the results using the URL(s) provided above.

Thank you for using Astro BEAM!

Best regards,
The Astro BEAM Team
""",
        _subtype="plain",
    )
