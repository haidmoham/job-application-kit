from __future__ import annotations

import hashlib
import re
from collections.abc import Mapping
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

TRACKING_QUERY_PREFIXES = ("utm_", "ref", "source", "trk", "tracking")
IDENTITY_QUERY_KEYS = {"id", "gh_jid", "jobid", "job_id", "requisitionid", "reqid"}


def normalize_text(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def canonicalize_url(url: str) -> str:
    """Remove tracking noise while preserving parameters that can identify a requisition."""
    raw = url.strip()
    if not raw:
        return ""
    try:
        parts = urlsplit(raw)
    except ValueError:
        return raw

    host = parts.netloc.lower().removeprefix("www.")
    path = re.sub(r"/+", "/", parts.path).rstrip("/") or "/"
    kept: list[tuple[str, str]] = []
    for key, value in parse_qsl(parts.query, keep_blank_values=False):
        lower = key.lower()
        if lower in IDENTITY_QUERY_KEYS:
            kept.append((lower, value))
        elif any(lower.startswith(prefix) for prefix in TRACKING_QUERY_PREFIXES):
            continue
    return urlunsplit((parts.scheme.lower() or "https", host, path, urlencode(sorted(kept)), ""))


def job_fingerprint(company: str, title: str, location: str = "") -> str:
    seed = "|".join(
        [normalize_text(company), normalize_text(title), normalize_text(location or "remote")]
    )
    return hashlib.sha256(seed.encode()).hexdigest()[:20]


def identity_keys(job: Mapping[str, object]) -> set[str]:
    keys: set[str] = set()
    url = canonicalize_url(str(job.get("url") or ""))
    if url:
        keys.add(f"url:{url}")
    keys.add(
        "role:"
        + job_fingerprint(
            str(job.get("company") or ""),
            str(job.get("title") or ""),
            str(job.get("location") or ""),
        )
    )
    return keys


def is_duplicate(job: Mapping[str, object], seen_keys: set[str]) -> bool:
    return bool(identity_keys(job) & seen_keys)
