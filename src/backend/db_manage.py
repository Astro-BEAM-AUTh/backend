"""Database management CLI for schema and migration operations."""

from __future__ import annotations

import argparse
import asyncio
import re
from datetime import UTC, datetime
from io import StringIO
from pathlib import Path
from typing import Protocol, TextIO

from alembic import command
from alembic.config import Config
from sqlalchemy import text
from sqlalchemy.engine import URL, make_url
from sqlalchemy.ext.asyncio import create_async_engine

from backend.configs.config import settings

_DATE_REVISION_PATTERN = re.compile(r"^(?P<date>\d{8})_(?P<counter>\d{4})$")


class _AlembicScriptLike(Protocol):
    revision: str
    down_revision: str | tuple[str, ...] | None


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _build_alembic_config(stdout: TextIO | None = None) -> Config:
    root = _project_root()
    config = Config(str(root / "alembic.ini"), stdout=stdout)
    config.set_main_option("script_location", str(root / "migrations"))
    config.set_main_option("sqlalchemy.url", str(settings.database_url))
    if stdout is not None:
        # Alembic offline SQL emission uses output_buffer from attributes.
        config.attributes["output_buffer"] = stdout
    return config


def _next_date_revision_id() -> str:
    today = datetime.now(UTC).strftime("%Y%m%d")
    versions_dir = _project_root() / "migrations" / "versions"

    max_counter = 0
    for path in versions_dir.glob("*.py"):
        prefix = path.stem.split("_", maxsplit=2)
        if len(prefix) < 2:
            continue

        candidate = f"{prefix[0]}_{prefix[1]}"
        match = _DATE_REVISION_PATTERN.fullmatch(candidate)
        if match is None:
            continue

        if match.group("date") != today:
            continue

        max_counter = max(max_counter, int(match.group("counter")))

    return f"{today}_{max_counter + 1:04d}"


def _normalize_down_revision(down_revision: str | tuple[str, ...] | None) -> str | None:
    if down_revision is None:
        return None

    if isinstance(down_revision, str):
        return down_revision

    if isinstance(down_revision, tuple):
        if len(down_revision) == 1:
            value = down_revision[0]
            if isinstance(value, str):
                return value
        msg = "Generating SQL for merge revisions is not supported automatically."
        raise ValueError(msg)

    msg = f"Unsupported down_revision type: {type(down_revision)!r}"
    raise TypeError(msg)


def _write_sql_file(path: Path, header: str, sql_text: str) -> None:
    path.write_text(f"-- {header}\n\n{sql_text}", encoding="utf-8")


def _generate_sql_for_revision(script: _AlembicScriptLike) -> None:
    revision_id = getattr(script, "revision", None)
    down_revision = _normalize_down_revision(getattr(script, "down_revision", None))

    if not isinstance(revision_id, str):
        msg = "Could not resolve revision id from generated script."
        raise TypeError(msg)

    sql_dir = _project_root() / "migrations" / "versions" / "sql"
    sql_dir.mkdir(parents=True, exist_ok=True)

    upgrade_buffer = StringIO()
    command.upgrade(
        _build_alembic_config(stdout=upgrade_buffer),
        f"{down_revision or 'base'}:{revision_id}",
        sql=True,
    )
    _write_sql_file(
        sql_dir / f"{revision_id}_upgrade.sql",
        f"Upgrade SQL for revision {revision_id}",
        upgrade_buffer.getvalue(),
    )

    downgrade_buffer = StringIO()
    command.downgrade(
        _build_alembic_config(stdout=downgrade_buffer),
        f"{revision_id}:{down_revision or 'base'}",
        sql=True,
    )
    _write_sql_file(
        sql_dir / f"{revision_id}_downgrade.sql",
        f"Downgrade SQL for revision {revision_id}",
        downgrade_buffer.getvalue(),
    )


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="backend-db",
        description="Manage PostgreSQL database creation and Alembic migrations.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("create-db", help="Create the target PostgreSQL database if it does not exist.")

    init_parser = subparsers.add_parser("init", help="Create database if needed and apply all migrations.")
    init_parser.add_argument("--revision", default="head", help="Target migration revision (default: head).")

    upgrade_parser = subparsers.add_parser("upgrade", help="Upgrade database schema to a target revision.")
    upgrade_parser.add_argument("revision", nargs="?", default="head", help="Target revision (default: head).")

    downgrade_parser = subparsers.add_parser("downgrade", help="Downgrade database schema to a target revision.")
    downgrade_parser.add_argument("revision", help="Target revision (e.g. -1, base, 20260505_0001).")

    revision_parser = subparsers.add_parser("revision", help="Create a new migration revision.")
    revision_parser.add_argument("-m", "--message", required=True, help="Migration message.")
    revision_parser.add_argument("--autogenerate", action="store_true", help="Auto-generate migration operations from model changes.")
    revision_parser.add_argument("--rev-id", help="Revision identifier. Defaults to YYYYMMDD_NNNN.")
    revision_parser.add_argument(
        "--no-sql",
        action="store_true",
        help="Do not generate SQL files for the revision under migrations/versions/sql.",
    )

    stamp_parser = subparsers.add_parser("stamp", help="Mark database with a migration version without applying migrations.")
    stamp_parser.add_argument("revision", help="Revision to stamp.")

    subparsers.add_parser("current", help="Show current migration version.")
    subparsers.add_parser("history", help="Show migration history.")

    return parser.parse_args()


def _postgres_admin_url(database_url: URL) -> URL:
    return database_url.set(database="postgres")


async def _create_database_if_not_exists() -> None:
    database_url = make_url(str(settings.database_url))
    db_name = database_url.database

    if not db_name:
        msg = "DATABASE_URL must include a database name."
        raise ValueError(msg)

    admin_url = _postgres_admin_url(database_url)
    engine = create_async_engine(
        admin_url.render_as_string(hide_password=False),
        echo=settings.db_echo,
        isolation_level="AUTOCOMMIT",
    )

    try:
        async with engine.connect() as conn:
            exists = await conn.scalar(
                text("SELECT 1 FROM pg_database WHERE datname = :database_name"),
                {"database_name": db_name},
            )
            if exists:
                print(f"Database '{db_name}' already exists.")
                return

            escaped_db_name = db_name.replace('"', '""')
            await conn.execute(text(f'CREATE DATABASE "{escaped_db_name}"'))
            print(f"Created database '{db_name}'.")
    finally:
        await engine.dispose()


def main() -> None:
    args = _parse_args()
    config = _build_alembic_config()

    if args.command == "create-db":
        asyncio.run(_create_database_if_not_exists())
        return

    if args.command == "init":
        asyncio.run(_create_database_if_not_exists())
        command.upgrade(config, args.revision)
        return

    if args.command == "upgrade":
        command.upgrade(config, args.revision)
        return

    if args.command == "downgrade":
        command.downgrade(config, args.revision)
        return

    if args.command == "revision":
        revision_id = args.rev_id or _next_date_revision_id()
        script = command.revision(
            config,
            message=args.message,
            autogenerate=args.autogenerate,
            rev_id=revision_id,
        )

        if not args.no_sql:
            if isinstance(script, list):
                for item in script:
                    if item is not None:
                        _generate_sql_for_revision(item)
            elif script is not None:
                _generate_sql_for_revision(script)
        return

    if args.command == "stamp":
        command.stamp(config, args.revision)
        return

    if args.command == "current":
        command.current(config)
        return

    if args.command == "history":
        command.history(config)
        return

    msg = f"Unsupported command: {args.command}"
    raise ValueError(msg)


if __name__ == "__main__":
    main()
