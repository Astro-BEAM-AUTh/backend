-- Upgrade SQL for revision 20260601_0001

BEGIN;

CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL, 
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Running upgrade  -> 20260601_0001

CREATE TYPE observationstatusenum AS ENUM ('PENDING', 'IN_PROGRESS', 'COMPLETED', 'FAILED', 'CANCELLED');

CREATE TYPE observationtypeenum AS ENUM ('HOT_CALIBRATION', 'COLD_CALIBRATION', 'TARGET_OBSERVATION');

CREATE TYPE referenceframeenum AS ENUM ('TOPO', 'LSRK', 'BARY', 'HELIO', 'GEO');

CREATE TYPE centralfrequencyenum AS ENUM ('FREQ_1420_MHZ', 'FREQ_1670_MHZ', 'FREQ_22000_MHZ');

CREATE TYPE bandwidthenum AS ENUM ('BW_1_5_MHZ', 'BW_1_75_MHZ', 'BW_2_5_MHZ', 'BW_2_75_MHZ', 'BW_3_MHZ', 'BW_3_84_MHZ', 'BW_5_5_MHZ', 'BW_6_MHZ', 'BW_7_MHZ', 'BW_8_75_MHZ', 'BW_10_MHZ', 'BW_12_MHZ', 'BW_14_MHZ', 'BW_20_MHZ', 'BW_28_MHZ');

CREATE TABLE users (
    user_id VARCHAR NOT NULL, 
    username VARCHAR NOT NULL, 
    email VARCHAR NOT NULL, 
    auth_provider VARCHAR NOT NULL, 
    id SERIAL NOT NULL, 
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
    updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
    is_active BOOLEAN NOT NULL, 
    PRIMARY KEY (id)
);

CREATE INDEX ix_users_auth_provider ON users (auth_provider);

CREATE UNIQUE INDEX ix_users_email ON users (email);

CREATE UNIQUE INDEX ix_users_user_id ON users (user_id);

CREATE INDEX ix_users_username ON users (username);

CREATE TABLE observations (
    target_name VARCHAR(255), 
    ra FLOAT NOT NULL, 
    dec FLOAT NOT NULL, 
    bandwidth bandwidthenum DEFAULT 'BW_1_5_MHZ' NOT NULL, 
    center_frequency centralfrequencyenum DEFAULT 'FREQ_1420_MHZ' NOT NULL, 
    velocity_frame referenceframeenum DEFAULT 'LSRK' NOT NULL, 
    observation_type observationtypeenum DEFAULT 'TARGET_OBSERVATION' NOT NULL, 
    fft_size INTEGER DEFAULT 1024 NOT NULL, 
    integration_time FLOAT NOT NULL, 
    planned_start TIMESTAMP WITHOUT TIME ZONE, 
    output_filename VARCHAR(1000) NOT NULL, 
    receive_csv BOOLEAN DEFAULT false NOT NULL, 
    perform_data_analysis BOOLEAN DEFAULT true NOT NULL, 
    id SERIAL NOT NULL, 
    user_id INTEGER NOT NULL, 
    status observationstatusenum DEFAULT 'PENDING' NOT NULL, 
    completed_on TIMESTAMP WITHOUT TIME ZONE, 
    created_on TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL, 
    updated_on TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL, 
    PRIMARY KEY (id), 
    CONSTRAINT ck_observations_dec_range CHECK (dec >= -90 AND dec <= 90), 
    CONSTRAINT ck_observations_integration_time_positive CHECK (integration_time > 0), 
    CONSTRAINT ck_observations_ra_range CHECK (ra >= 0 AND ra < 360), 
    FOREIGN KEY(user_id) REFERENCES users (id)
);

INSERT INTO alembic_version (version_num) VALUES ('20260601_0001') RETURNING alembic_version.version_num;

COMMIT;

