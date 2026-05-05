"""initial schema

Revision ID: 20260505_0001
Revises: None
Create Date: 2026-05-05 00:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "20260505_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_user_id"), "users", ["user_id"], unique=True)
    op.create_index(op.f("ix_users_username"), "users", ["username"], unique=True)

    op.create_table(
        "observations",
        sa.Column("target_name", sa.String(), nullable=False),
        sa.Column("observation_object", sa.String(), nullable=False),
        sa.Column("ra", sa.Float(), nullable=False),
        sa.Column("dec", sa.Float(), nullable=False),
        sa.Column("center_frequency", sa.Float(), nullable=False),
        sa.Column("rf_gain", sa.Float(), nullable=False),
        sa.Column("if_gain", sa.Float(), nullable=False),
        sa.Column("bb_gain", sa.Float(), nullable=False),
        sa.Column("observation_type", sa.String(), nullable=False),
        sa.Column("integration_time", sa.Float(), nullable=False),
        sa.Column("output_filename", sa.String(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("observation_id", sa.String(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("submitted_at", sa.DateTime(), nullable=False),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_observations_observation_id"), "observations", ["observation_id"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_observations_observation_id"), table_name="observations")
    op.drop_table("observations")

    op.drop_index(op.f("ix_users_username"), table_name="users")
    op.drop_index(op.f("ix_users_user_id"), table_name="users")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
