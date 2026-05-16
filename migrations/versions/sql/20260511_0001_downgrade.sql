-- Downgrade SQL for revision 20260511_0001

BEGIN;

-- Running downgrade 20260511_0001 -> 20260510_0001

DROP INDEX ix_users_auth_provider;

DROP INDEX ix_users_username;

CREATE UNIQUE INDEX ix_users_username ON users (username);

ALTER TABLE users DROP COLUMN auth_provider;

UPDATE alembic_version SET version_num='20260510_0001' WHERE alembic_version.version_num = '20260511_0001';

COMMIT;

