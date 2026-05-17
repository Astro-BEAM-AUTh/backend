-- Upgrade SQL for revision 20260506_0001

BEGIN;

CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL, 
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Running upgrade  -> 20260506_0001

CREATE TYPE observationstatus AS ENUM ('PENDING', 'IN_PROGRESS', 'COMPLETED', 'FAILED', 'CANCELLED');

CREATE TABLE users (
    user_id VARCHAR NOT NULL, 
    username VARCHAR NOT NULL, 
    email VARCHAR NOT NULL, 
    id SERIAL NOT NULL, 
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
    updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
    is_active BOOLEAN NOT NULL, 
    PRIMARY KEY (id)
);

CREATE UNIQUE INDEX ix_users_email ON users (email);

CREATE UNIQUE INDEX ix_users_user_id ON users (user_id);

CREATE UNIQUE INDEX ix_users_username ON users (username);

CREATE TABLE observations (
    target_name VARCHAR(255) NOT NULL, 
    observation_object VARCHAR(255) NOT NULL, 
    ra FLOAT NOT NULL, 
    dec FLOAT NOT NULL, 
    center_frequency FLOAT NOT NULL, 
    rf_gain FLOAT NOT NULL, 
    if_gain FLOAT NOT NULL, 
    bb_gain FLOAT NOT NULL, 
    observation_type VARCHAR(100) NOT NULL, 
    integration_time FLOAT NOT NULL, 
    output_filename VARCHAR(1000) NOT NULL, 
    id SERIAL NOT NULL, 
    observation_id VARCHAR(255) NOT NULL, 
    user_id INTEGER NOT NULL, 
    status observationstatus NOT NULL, 
    submitted_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
    completed_at TIMESTAMP WITHOUT TIME ZONE, 
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
    updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
    PRIMARY KEY (id), 
    CONSTRAINT ck_observations_center_frequency_positive CHECK (center_frequency > 0), 
    CONSTRAINT ck_observations_dec_range CHECK (dec >= -90 AND dec <= 90), 
    CONSTRAINT ck_observations_integration_time_positive CHECK (integration_time > 0), 
    CONSTRAINT ck_observations_ra_range CHECK (ra >= 0 AND ra < 360), 
    FOREIGN KEY(user_id) REFERENCES users (id)
);

CREATE UNIQUE INDEX ix_observations_observation_id ON observations (observation_id);

INSERT INTO alembic_version (version_num) VALUES ('20260506_0001') RETURNING alembic_version.version_num;

COMMIT;

