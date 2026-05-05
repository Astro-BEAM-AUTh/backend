-- Downgrade SQL for revision 20260505_0001

BEGIN;

-- Running downgrade 20260505_0001 -> 

DROP INDEX ix_observations_observation_id;

DROP TABLE observations;

DROP INDEX ix_users_username;

DROP INDEX ix_users_user_id;

DROP INDEX ix_users_email;

DROP TABLE users;

DROP TYPE observationstatus;

DELETE FROM alembic_version WHERE alembic_version.version_num = '20260505_0001';

DROP TABLE alembic_version;

COMMIT;

