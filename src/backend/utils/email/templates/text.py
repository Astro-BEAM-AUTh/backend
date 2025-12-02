from backend.models.observation import Observation
from backend.models.user import User


def create_text_email_body_for_confirmation(observation: Observation, user: User) -> str:
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


def create_text_email_body_for_completion(observation: Observation, user: User) -> str:
    """Create plain text email body for observation completion."""
    if observation.completed_at is None:
        msg = "Cannot create completion email for observation without completed_at timestamp"
        raise ValueError(msg)
    duration = (observation.completed_at - observation.submitted_at).total_seconds() / 3600 if observation.completed_at else 0

    return f"""
Dear {user.username},

Great news! Your observation has been completed successfully!

Observation Details:
-------------------
Observation ID: {observation.observation_id}
Target Name: {observation.target_name}
Object: {observation.observation_object}
Coordinates: RA {observation.ra}°, Dec {observation.dec}°
Center Frequency: {observation.center_frequency} MHz
Integration Time: {observation.integration_time} seconds
Observation Type: {observation.observation_type}
Output File: {observation.output_filename}
Status: {observation.status}
Submitted At: {observation.submitted_at.strftime("%Y-%m-%d %H:%M:%S UTC")}
Completed At: {observation.completed_at.strftime("%Y-%m-%d %H:%M:%S UTC") if observation.completed_at else "N/A"}
Processing Duration: {duration:.2f} hours

Your observation data is now ready for analysis. You can access the results using the output filename provided above.

Thank you for using Astro BEAM!

Best regards,
The Astro BEAM Team
"""
