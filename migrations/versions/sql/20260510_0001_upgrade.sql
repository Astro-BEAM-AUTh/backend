-- Upgrade SQL for revision 20260510_0001

BEGIN;

-- Running upgrade 20260506_0001 -> 20260510_0001

CREATE TYPE observationtype AS ENUM ('HOT_CALIBRATION', 'COLD_CALIBRATION', 'TARGET_OBSERVATION');

UPDATE observations
SET observation_type = CASE
    WHEN observation_type IN ('HOT_CALIBRATION', 'hot_calibration', 'HotCalibration', 'hot calibration', 'hot-calibration')
        THEN 'HOT_CALIBRATION'
    WHEN observation_type IN ('COLD_CALIBRATION', 'cold_calibration', 'ColdCalibration', 'cold calibration', 'cold-calibration')
        THEN 'COLD_CALIBRATION'
    WHEN observation_type IN ('TARGET_OBSERVATION', 'target_observation', 'TargetObservation', 'target observation', 'target-observation')
        THEN 'TARGET_OBSERVATION'
    ELSE observation_type
END
WHERE observation_type IS NOT NULL;

ALTER TABLE observations ALTER COLUMN observation_type TYPE observationtype USING observation_type::observationtype;

UPDATE alembic_version SET version_num='20260510_0001' WHERE alembic_version.version_num = '20260506_0001';

COMMIT;

