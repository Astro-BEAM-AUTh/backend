-- Upgrade SQL for revision 20260511_0001

BEGIN;

-- Running upgrade 20260510_0001 -> 20260511_0001

ALTER TABLE users ADD COLUMN auth_provider VARCHAR NOT NULL DEFAULT 'guest';

DROP INDEX ix_users_username;

CREATE INDEX ix_users_username ON users (username);

CREATE INDEX ix_users_auth_provider ON users (auth_provider);

UPDATE alembic_version SET version_num='20260511_0001' WHERE alembic_version.version_num = '20260510_0001';

COMMIT;

