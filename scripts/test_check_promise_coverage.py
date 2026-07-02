#!/usr/bin/env python3
"""Fixture tests for the promise-coverage gate (stdlib unittest, zero-dep)."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_promise_coverage as g  # noqa: E402


class PromiseCoverage(unittest.TestCase):
    def test_linked_promise_passes(self):
        self.assertEqual(g.check({
            "known_tests": ["ac-1"],
            "promises": [{"id": "p1", "test_ref": "ac-1", "universal": False}],
        }), [])

    def test_unlinked_promise_blocks(self):
        self.assertTrue(g.check({
            "known_tests": ["ac-1"],
            "promises": [{"id": "p1", "test_ref": None}],
        }))

    def test_dangling_ref_blocks(self):
        self.assertTrue(g.check({
            "known_tests": ["ac-1"],
            "promises": [{"id": "p1", "test_ref": "ac-99"}],
        }))

    def test_universal_without_boundary_blocks(self):
        fails = g.check({
            "known_tests": ["ac-1"],
            "promises": [{"id": "floor", "test_ref": "ac-1", "universal": True, "boundary": False}],
        })
        self.assertTrue(fails)
        self.assertIn("boundary", fails[0])

    def test_universal_with_boundary_passes(self):
        self.assertEqual(g.check({
            "known_tests": ["ac-1"],
            "promises": [{"id": "floor", "test_ref": "ac-1", "universal": True, "boundary": True}],
        }), [])

    def test_no_promises_passes(self):
        self.assertEqual(g.check({"known_tests": [], "promises": []}), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
