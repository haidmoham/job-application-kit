from __future__ import annotations

import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from .dedupe import canonicalize_url

DEFAULT_PATH = Path.home() / ".local" / "share" / "job-application-kit" / "history.db"


def database_path() -> Path:
    override = os.environ.get("JOB_APPLICATION_HISTORY", "").strip()
    return Path(override).expanduser() if override else DEFAULT_PATH


def connect(path: Path | None = None) -> sqlite3.Connection:
    db_path = path or database_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            canonical_url TEXT NOT NULL UNIQUE,
            company TEXT NOT NULL,
            title TEXT NOT NULL,
            location TEXT,
            lane TEXT,
            resume TEXT,
            submitted_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    return conn


def already_submitted(url: str, conn: sqlite3.Connection | None = None) -> bool:
    canonical = canonicalize_url(url)
    if not canonical:
        return False
    owned = conn is None
    conn = conn or connect()
    try:
        return conn.execute(
            "SELECT 1 FROM applications WHERE canonical_url = ? LIMIT 1", (canonical,)
        ).fetchone() is not None
    finally:
        if owned:
            conn.close()


def record_submission(
    *,
    url: str,
    company: str,
    title: str,
    location: str | None = None,
    lane: str | None = None,
    resume: str | None = None,
    conn: sqlite3.Connection | None = None,
) -> None:
    canonical = canonicalize_url(url)
    if not canonical:
        raise ValueError("A valid job URL is required to record a submission.")
    owned = conn is None
    conn = conn or connect()
    try:
        conn.execute(
            """
            INSERT INTO applications (canonical_url, company, title, location, lane, resume, submitted_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(canonical_url) DO NOTHING
            """,
            (
                canonical,
                company,
                title,
                location,
                lane,
                resume,
                datetime.now(timezone.utc).isoformat(timespec="seconds"),
            ),
        )
        conn.commit()
    finally:
        if owned:
            conn.close()
