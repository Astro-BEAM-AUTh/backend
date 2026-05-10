from enum import StrEnum


class ObservationType(StrEnum):
    """Enumeration for the type of an observation."""

    HOT_CALIBRATION = "hot_calibration"
    COLD_CALIBRATION = "cold_calibration"
    TARGET_OBSERVATION = "target_observation"
