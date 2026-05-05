from enum import StrEnum


class ObservationStatus(StrEnum):
    """Enumeration for the status of an observation."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
