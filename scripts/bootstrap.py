from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config"
FILES = ("profile", "resumes", "searches", "application-state")


def main() -> int:
    for name in FILES:
        source = CONFIG / f"{name}.example.toml"
        target = CONFIG / f"{name}.toml"
        if target.exists():
            print(f"keep   {target.relative_to(ROOT)}")
            continue
        shutil.copyfile(source, target)
        print(f"create {target.relative_to(ROOT)}")
    print("\nNext: invoke job-search-onboarding and provide your current resume when requested.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
