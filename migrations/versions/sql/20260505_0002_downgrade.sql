BEGIN;

-- Running downgrade 20260505_0002 -> 20260505_0001

ALTER TABLE observations ALTER COLUMN status TYPE VARCHAR;

DROP TYPE observationstatus;

UPDATE alembic_version SET version_num='20260505_0001' WHERE alembic_version.version_num = '20260505_0002';

COMMIT;

