import tempfile
import unittest
from pathlib import Path

from job_application_kit.history import already_submitted, connect, record_submission


class HistoryTests(unittest.TestCase):
    def test_record_and_dedupe_submission(self):
        with tempfile.TemporaryDirectory() as directory:
            conn = connect(Path(directory) / "history.db")
            try:
                record_submission(url="https://example.com/job/1?utm_source=x", company="A", title="Engineer", conn=conn)
                self.assertTrue(already_submitted("https://example.com/job/1", conn=conn))
            finally:
                conn.close()


if __name__ == "__main__":
    unittest.main()
