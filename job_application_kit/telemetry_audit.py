from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

from .telemetry import telemetry_path


def load_records(path: Path | None = None) -> list[dict[str, Any]]:
    source = path or telemetry_path()
    if not source.exists():
        return []
    rows: list[dict[str, Any]] = []
    with source.open(encoding="utf-8") as handle:
        for number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as error:
                raise ValueError(f"Invalid JSON on line {number} of {source}.") from error
            if not isinstance(row, dict):
                raise ValueError(f"Telemetry line {number} must be a JSON object.")
            rows.append(row)
    return rows


def summarize(records: Iterable[dict[str, Any]]) -> dict[str, Any]:
    rows = list(records)
    outcomes = Counter(str(row.get("outcome") or "incomplete") for row in rows)
    durations = [int(row.get("wall_clock_ms") or 0) for row in rows]
    return {
        "records": len(rows),
        "outcomes": dict(sorted(outcomes.items())),
        "wall_clock_ms_total": sum(durations),
        "average_wall_clock_ms": round(sum(durations) / len(durations)) if durations else 0,
        "human_interventions": sum(int(row.get("human_interventions") or 0) for row in rows),
        "browser_actions": sum(int(row.get("browser_actions") or 0) for row in rows),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Summarize local job-application telemetry.")
    parser.add_argument("path", nargs="?", type=Path, default=None)
    args = parser.parse_args(argv)
    print(json.dumps(summarize(load_records(args.path)), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
