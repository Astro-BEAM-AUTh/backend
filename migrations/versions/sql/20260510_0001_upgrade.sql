-- Upgrade SQL for revision 20260510_0001

BEGIN;

-- Running upgrade 20260506_0001 -> 20260510_0001

CREATE TYPE observationtype AS ENUM ('HOT_CALIBRATION', 'COLD_CALIBRATION', 'TARGET_OBSERVATION');

ALTER TABLE observations ALTER COLUMN observation_type TYPE observationtype USING observation_type::observationtype;

UPDATE alembic_version SET version_num='20260510_0001' WHERE alembic_version.version_num = '20260506_0001';

COMMIT;

