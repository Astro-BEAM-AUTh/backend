-- Downgrade SQL for revision 20260510_0001

BEGIN;

-- Running downgrade 20260510_0001 -> 20260506_0001

ALTER TABLE observations ALTER COLUMN observation_type TYPE VARCHAR(100);

DROP TYPE observationtype;

UPDATE alembic_version SET version_num='20260506_0001' WHERE alembic_version.version_num = '20260510_0001';

COMMIT;

