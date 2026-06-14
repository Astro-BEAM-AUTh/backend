-- Downgrade SQL for revision 20260601_0001

BEGIN;

-- Running downgrade 20260601_0001 -> 

DROP TABLE observations;

DROP INDEX ix_users_username;

DROP INDEX ix_users_user_id;

DROP INDEX ix_users_email;

DROP INDEX ix_users_auth_provider;

DROP TABLE users;

DROP TYPE bandwidthenum;

DROP TYPE centralfrequencyenum;

DROP TYPE referenceframeenum;

DROP TYPE observationtypeenum;

DROP TYPE observationstatusenum;

DELETE FROM alembic_version WHERE alembic_version.version_num = '20260601_0001';

DROP TABLE alembic_version;

COMMIT;

