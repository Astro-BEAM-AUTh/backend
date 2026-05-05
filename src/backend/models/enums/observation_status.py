from enum import Enum


class ObservationStatus(str, Enum):
    """Enumeration for the status of an observation."""

    PENDING = "pending"
    IN_PROGRESS = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
