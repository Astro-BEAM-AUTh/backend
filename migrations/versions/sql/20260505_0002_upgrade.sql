BEGIN;

-- Running upgrade 20260505_0001 -> 20260505_0002

CREATE TYPE observationstatus AS ENUM ('PENDING', 'IN_PROGRESS', 'COMPLETED', 'FAILED', 'CANCELLED');

ALTER TABLE observations ALTER COLUMN status TYPE observationstatus USING status::observationstatus;

UPDATE alembic_version SET version_num='20260505_0002' WHERE alembic_version.version_num = '20260505_0001';

COMMIT;

