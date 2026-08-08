import unittest

from job_application_kit.dedupe import canonicalize_url, identity_keys


class DedupeTests(unittest.TestCase):
    def test_drops_tracking_but_keeps_requisition_id(self):
        url = "https://example.com/jobs/123/?utm_source=x&job_id=44&ref=abc"
        self.assertEqual("https://example.com/jobs/123?job_id=44", canonicalize_url(url))

    def test_role_identity_is_stable(self):
        left = identity_keys({"company": "Example Co", "title": "Backend Engineer", "location": "Remote"})
        right = identity_keys({"company": "example co", "title": "Backend-Engineer", "location": "remote"})
        self.assertTrue(left & right)


if __name__ == "__main__":
    unittest.main()
