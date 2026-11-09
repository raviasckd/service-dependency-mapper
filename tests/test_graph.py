"""Tests for dependency graph validation and ordering."""

import unittest

from service_mapper.graph import build_plan


class DependencyGraphTests(unittest.TestCase):
    def test_builds_stable_deployment_layers(self) -> None:
        plan = build_plan({"services": [
            {"name": "worker", "depends_on": ["api"]},
            {"name": "database", "depends_on": []},
            {"name": "api", "depends_on": ["database"]},
        ]})
        self.assertEqual(plan["layers"], [["database"], ["api"], ["worker"]])
        self.assertEqual(plan["dependency_count"], 2)

    def test_rejects_unknown_dependency(self) -> None:
        with self.assertRaisesRegex(ValueError, "unknown dependencies"):
            build_plan({"services": [{"name": "api", "depends_on": ["missing"]}]})

    def test_detects_cycles(self) -> None:
        document = {"services": [
            {"name": "api", "depends_on": ["worker"]},
            {"name": "worker", "depends_on": ["api"]},
        ]}
        with self.assertRaisesRegex(ValueError, "cycle detected"):
            build_plan(document)

    def test_rejects_duplicate_names(self) -> None:
        with self.assertRaisesRegex(ValueError, "duplicate service name"):
            build_plan({"services": [{"name": "api"}, {"name": "api"}]})


if __name__ == "__main__":
    unittest.main()
