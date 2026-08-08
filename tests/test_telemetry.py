import json
import tempfile
import unittest
from pathlib import Path

from job_application_kit.telemetry import start_run
from job_application_kit.telemetry_audit import load_records, summarize


class TelemetryTests(unittest.TestCase):
    def test_writes_and_summarizes(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "telemetry.jsonl"
            run = start_run(path=path, company="Example", title="Engineer")
            run.mark_stage("form")
            run.add_browser_action(3)
            run.safe_finish("submitted")
            records = load_records(path)
            self.assertEqual(1, len(records))
            self.assertEqual("submitted", records[0]["outcome"])
            self.assertEqual(3, summarize(records)["browser_actions"])

    def test_fail_open_on_bad_destination(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "directory"
            destination.mkdir()
            run = start_run(path=destination)
            self.assertIsNotNone(run.safe_finish("submitted"))
            self.assertIsNotNone(run.write_error)


if __name__ == "__main__":
    unittest.main()
