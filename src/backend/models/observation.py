"""Telescope observation database model."""

from datetime import datetime

from sqlalchemy import event
from sqlmodel import CheckConstraint, Field, Relationship, SQLModel, String
from sqlmodel._compat import SQLModelConfig

from backend.models.enums.observation_status import ObservationStatus
from backend.models.enums.observation_type import ObservationType
from backend.models.user import User, UserCreate
from backend.utils.time_utils import utc_now


class ObservationBase(SQLModel):
    """Base model for telescope observations shared between API and database."""

    # Observation target information
    target_name: str = Field(description="Name of the observation target", sa_type=String(255))
    observation_object: str = Field(description="Object being observed", sa_type=String(255))
    ra: float = Field(description="Right Ascension in degrees")
    dec: float = Field(description="Declination in degrees")

    # Telescope configuration
    center_frequency: float = Field(description="Center frequency in MHz")
    rf_gain: float = Field(description="RF gain in dB")
    if_gain: float = Field(description="IF gain in dB")
    bb_gain: float = Field(description="Baseband gain in dB")
    observation_type: ObservationType = Field(description="Type of observation", default=ObservationType.TARGET_OBSERVATION)
    integration_time: float = Field(description="Integration time in seconds")

    # Output information
    output_filename: str = Field(description="Filename for the observation data", sa_type=String(1000))

    model_config: SQLModelConfig = {
        "json_schema_extra": {
            "example": {
                "target_name": "M31",
                "observation_object": "Andromeda Galaxy",
                "ra": 10.68470833,
                "dec": 41.26875,
                "center_frequency": 1400.0,
                "rf_gain": 30.0,
                "if_gain": 20.0,
                "bb_gain": 10.0,
                "observation_type": "TARGET_OBSERVATION",
                "integration_time": 600.0,
                "output_filename": "m31_observation.fits",
            },
        },
    }


class ObservationCreate(ObservationBase):
    """Schema for creating a new observation (API request)."""


class ObservationRead(ObservationBase):
    """Schema for reading an observation (API response)."""

    observation_id: str = Field(description="Unique observation identifier")
    user_id: int = Field(description="ID of the user who submitted the observation")
    status: ObservationStatus = Field(description="Current observation status")
    submitted_at: datetime = Field(description="Timestamp of submission")
    completed_at: datetime | None = Field(default=None, description="Timestamp of completion")

    model_config: SQLModelConfig = {
        "json_schema_extra": {
            "example": {
                "observation_id": "obs_20231110_001",
                "user_id": 42,
                "target_name": "M31",
                "observation_object": "Andromeda Galaxy",
                "ra": 10.68470833,
                "dec": 41.26875,
                "center_frequency": 1400.0,
                "rf_gain": 30.0,
                "if_gain": 20.0,
                "bb_gain": 10.0,
                "observation_type": "TARGET_OBSERVATION",
                "integration_time": 600.0,
                "output_filename": "m31_observation.fits",
                "status": "PENDING",
                "submitted_at": "2023-11-10T12:34:56Z",
                "completed_at": None,
            },
        },
    }


class ObservationSubmissionRequest(SQLModel):
    """Payload for submitting an observation request."""

    observation: ObservationCreate = Field(description="Observation submission payload")
    requestor: UserCreate | None = Field(default=None, description="Optional guest requestor metadata")


class Observation(ObservationBase, table=True):
    """Database model for telescope observations."""

    __tablename__ = "observations"
    __table_args__ = (
        CheckConstraint("ra >= 0 AND ra < 360", name="ck_observations_ra_range"),
        CheckConstraint("dec >= -90 AND dec <= 90", name="ck_observations_dec_range"),
        CheckConstraint("center_frequency > 0", name="ck_observations_center_frequency_positive"),
        CheckConstraint("integration_time > 0", name="ck_observations_integration_time_positive"),
    )

    id: int | None = Field(default=None, primary_key=True)
    observation_id: str = Field(unique=True, index=True, description="Unique observation identifier", sa_type=String(255))

    # User relationship
    user_id: int = Field(foreign_key="users.id", description="ID of the user who submitted the observation")
    user: User = Relationship(back_populates="observations")

    # Status tracking
    status: ObservationStatus = Field(default=ObservationStatus.PENDING, description="Current observation status")
    submitted_at: datetime = Field(default_factory=utc_now, description="Timestamp of submission")
    completed_at: datetime | None = Field(default=None, description="Timestamp of completion")

    # Additional metadata
    created_at: datetime = Field(default_factory=utc_now, description="Record creation timestamp")
    updated_at: datetime = Field(default_factory=utc_now, description="Record update timestamp")


@event.listens_for(Observation, "before_update")
def update_updated_at(_: object, __: object, target: Observation) -> None:
    """Automatically update the 'updated_at' timestamp on record update."""
    target.updated_at = utc_now()
