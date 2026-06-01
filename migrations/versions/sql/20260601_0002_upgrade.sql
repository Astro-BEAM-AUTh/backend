-- Upgrade SQL for revision 20260601_0002

BEGIN;

-- Running upgrade 20260601_0001 -> 20260601_0002

ALTER TABLE observations ADD COLUMN csv_download_url TEXT;

ALTER TABLE observations ADD COLUMN analysis_results_url TEXT;

ALTER TABLE observations ADD COLUMN data_download_url TEXT;

UPDATE alembic_version SET version_num='20260601_0002' WHERE alembic_version.version_num = '20260601_0001';

COMMIT;

