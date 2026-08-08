import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from job_application_kit.routing import route_posting

SEARCHES = '''
[defaults]
exclude_levels = ["staff"]
exclude_title_terms = []

[[lanes]]
name = "backend"
label = "Backend"
priority = 1
resume = "primary"
title_match_terms = ["backend engineer"]
match_terms = ["python", "api", "postgres"]
'''

RESUMES = '''
[primary]
label = "Primary"
path_env = "JOB_RESUME_PRIMARY"
'''


class RoutingTests(unittest.TestCase):
    def test_routes_configured_lane(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            searches = root / "searches.toml"
            resumes = root / "resumes.toml"
            resume_file = root / "resume.pdf"
            searches.write_text(SEARCHES)
            resumes.write_text(RESUMES)
            resume_file.write_text("placeholder")
            with patch.dict(os.environ, {"JOB_RESUME_PRIMARY": str(resume_file)}):
                route = route_posting(
                    "Backend Engineer",
                    "Python API and Postgres",
                    searches_path=searches,
                    resumes_path=resumes,
                )
            self.assertIsNotNone(route)
            self.assertEqual("primary", route.resume)
            self.assertEqual(str(resume_file), route.resume_path)

    def test_rejects_excluded_level(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            searches = root / "searches.toml"
            resumes = root / "resumes.toml"
            searches.write_text(SEARCHES)
            resumes.write_text(RESUMES)
            self.assertIsNone(
                route_posting("Staff Backend Engineer", "Python API", searches_path=searches, resumes_path=resumes)
            )


if __name__ == "__main__":
    unittest.main()
