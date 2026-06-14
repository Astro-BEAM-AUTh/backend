-- Downgrade SQL for revision 20260601_0002

BEGIN;

-- Running downgrade 20260601_0002 -> 20260601_0001

ALTER TABLE observations DROP COLUMN data_download_url;

ALTER TABLE observations DROP COLUMN analysis_results_url;

ALTER TABLE observations DROP COLUMN csv_download_url;

UPDATE alembic_version SET version_num='20260601_0001' WHERE alembic_version.version_num = '20260601_0002';

COMMIT;

