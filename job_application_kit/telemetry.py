"""Small fail-open telemetry primitives for computer-use application runs."""

from __future__ import annotations

import json
import os
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_PATH = Path.home() / ".local" / "share" / "job-application-kit" / "telemetry.jsonl"
VALID_OUTCOMES = {"submitted", "failed", "blocked", "skipped", "unverified", "incomplete"}


def telemetry_path() -> Path:
    override = os.environ.get("JOB_APPLICATION_TELEMETRY", "").strip()
    return Path(override).expanduser() if override else DEFAULT_PATH


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def _append(record: dict[str, Any], path: Path | None = None) -> str | None:
    destination = path or telemetry_path()
    try:
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n")
    except (OSError, TypeError, ValueError) as error:
        return f"{type(error).__name__}: {error}"
    return None


@dataclass
class RunTelemetry:
    path: Path | None = None
    run_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    company: str | None = None
    title: str | None = None
    ats: str | None = None
    lane: str | None = None
    resume: str | None = None
    attempt_number: int = 1
    started_at: str = field(default_factory=_now)
    _started_monotonic: float = field(default_factory=time.monotonic, repr=False)
    retries: int = 0
    browser_actions: int = 0
    human_interventions: int = 0
    last_stage: str | None = None
    write_error: str | None = field(default=None, init=False)
    _finished: bool = field(default=False, init=False, repr=False)

    def mark_stage(self, stage: str) -> None:
        if not stage.strip():
            raise ValueError("stage must not be empty")
        self.last_stage = stage.strip()

    def add_retry(self, count: int = 1) -> None:
        self.retries += max(0, int(count))

    def add_browser_action(self, count: int = 1) -> None:
        self.browser_actions += max(0, int(count))

    def add_human_intervention(self, count: int = 1) -> None:
        self.human_interventions += max(0, int(count))

    def finish(self, outcome: str, *, failure_category: str | None = None) -> dict[str, Any] | None:
        if self._finished:
            return None
        normalized = outcome.strip().lower()
        if normalized not in VALID_OUTCOMES:
            raise ValueError(f"invalid outcome: {outcome}")
        record = {
            "schema_version": 1,
            "run_id": self.run_id,
            "started_at": self.started_at,
            "finished_at": _now(),
            "wall_clock_ms": round((time.monotonic() - self._started_monotonic) * 1000),
            "company": self.company,
            "title": self.title,
            "ats": self.ats,
            "lane": self.lane,
            "resume": self.resume,
            "attempt_number": self.attempt_number,
            "last_stage": self.last_stage,
            "retries": self.retries,
            "browser_actions": self.browser_actions,
            "human_interventions": self.human_interventions,
            "outcome": normalized,
            "failure_category": failure_category,
        }
        self.write_error = _append(record, self.path)
        self._finished = True
        return record

    def safe_finish(self, outcome: str, *, failure_category: str | None = None) -> dict[str, Any] | None:
        try:
            return self.finish(outcome, failure_category=failure_category)
        except Exception as error:
            self.write_error = f"{type(error).__name__}: {error}"
            self._finished = True
            return None


def start_run(**kwargs: Any) -> RunTelemetry:
    return RunTelemetry(**kwargs)
