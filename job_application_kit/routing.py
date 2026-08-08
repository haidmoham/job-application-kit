from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Route:
    lane: str
    label: str
    resume: str
    resume_path: str | None
    matched_terms: tuple[str, ...]


def _load(path: Path) -> dict:
    with path.open("rb") as handle:
        return tomllib.load(handle)


def route_posting(
    title: str,
    description: str = "",
    *,
    searches_path: Path | None = None,
    resumes_path: Path | None = None,
) -> Route | None:
    searches_path = searches_path or ROOT / "config" / "searches.toml"
    resumes_path = resumes_path or ROOT / "config" / "resumes.toml"
    config = _load(searches_path)
    defaults = config.get("defaults", {})
    text = f"{title}\n{description}".lower()
    title_lower = title.lower()

    excluded = tuple(defaults.get("exclude_levels", [])) + tuple(defaults.get("exclude_title_terms", []))
    if any(term.lower() in title_lower for term in excluded):
        return None

    candidates: list[tuple[int, int, dict, tuple[str, ...]]] = []
    for lane in config.get("lanes", []):
        title_terms = tuple(lane.get("title_match_terms", []))
        if title_terms and not any(term.lower() in title_lower for term in title_terms):
            continue
        matched = tuple(term for term in lane.get("match_terms", []) if term.lower() in text)
        if not matched:
            continue
        candidates.append((len(matched), -int(lane.get("priority", 99)), lane, matched))

    if not candidates:
        return None

    _, _, lane, matched = max(candidates, key=lambda item: (item[0], item[1]))
    resume_key = lane["resume"]
    resumes = _load(resumes_path)
    resume_config = resumes.get(resume_key, {})
    env_name = resume_config.get("path_env")
    resume_path = os.environ.get(env_name) if env_name else None
    if resume_path and not Path(resume_path).expanduser().is_file():
        resume_path = None
    return Route(
        lane=lane["name"],
        label=lane["label"],
        resume=resume_key,
        resume_path=resume_path,
        matched_terms=matched,
    )
