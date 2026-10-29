#!/usr/bin/env python3
"""F-1 regression tests for Thai 'มล.' size unit (audit-only file).
Run against UNFIXED server.py -> expect FAILs (gap proof).
Run against FIXED server.py -> expect all PASS.
"""
import os, sys, types, unittest
stub = types.ModuleType("meta_api")
stub.call = lambda *a, **k: (500, {})
stub.call_multipart = lambda *a, **k: (500, {})
sys.modules["meta_api"] = stub
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import server

class TestMlUnit(unittest.TestCase):
    def test_ml_conflict_stripped(self):
        safe, removed = server.enforce_claims("ขนาด 500 มล.", "ขนาด 600 มล.", "th")
        self.assertEqual(safe, server.MIN_DESC["th"])
        self.assertTrue(any("size-mismatch" in r for r in removed))
    def test_ml_matching_kept(self):
        safe, removed = server.enforce_claims("ขนาด 500 มล.", "ขนาด 500 มล.", "th")
        self.assertIn("500 มล.", safe)
        self.assertEqual(removed, [])
    def test_ml_without_seller_facts_stripped(self):
        safe, removed = server.enforce_claims("ขนาด 500 มล.", "", "th")
        self.assertEqual(safe, server.MIN_DESC["th"])
        self.assertTrue(any("size-unverified" in r for r in removed))
    def test_no_size_text_unaffected(self):
        safe, removed = server.enforce_claims("อร่อยมาก พกพาง่าย", "", "th")
        self.assertEqual(safe, "อร่อยมาก พกพาง่าย")
        self.assertEqual(removed, [])
    def test_ml_without_dot_stripped(self):
        safe, removed = server.enforce_claims("ขนาด 500 มล", "", "th")
        self.assertEqual(safe, server.MIN_DESC["th"])
        self.assertTrue(any("size-unverified" in r for r in removed))

if __name__ == "__main__":
    unittest.main(verbosity=2)
