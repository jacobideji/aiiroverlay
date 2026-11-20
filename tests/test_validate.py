#!/usr/bin/env python3
"""Regression tests for the staleness checks in `scripts/validate.py`.

The 7-day `agent.last_reviewed` check read the field from the document root
from v0.14.0 through v0.42.1. The schema places it under `agent`, so the
check never evaluated: it reported the field missing whatever an AI-BOM
said, and no value could satisfy it. These tests pin the field's location so
the same defect cannot return without a red build.

Run: python3 -m unittest discover -s tests
"""

import importlib.util
import unittest
from datetime import date, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location(
    "ir_validate", REPO_ROOT / "scripts" / "validate.py"
)
validate = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(validate)

TODAY = date(2026, 11, 20)


def ai_bom(last_reviewed=None):
    """A minimal instance carrying only what the staleness check reads."""
    agent = {}
    if last_reviewed is not None:
        agent["last_reviewed"] = last_reviewed
    return {"agent": agent, "kill_switches": {"maturity_target": "level_1_aware"}}


def findings_for(instance):
    return [
        f
        for f in validate.check_staleness(instance, today=TODAY)
        if "last_reviewed" in f
    ]


class LastReviewedLocation(unittest.TestCase):
    def test_current_plain_date_under_agent_is_clean(self):
        self.assertEqual(findings_for(ai_bom(TODAY.isoformat())), [])

    def test_rfc3339_timestamp_under_agent_is_parsed(self):
        self.assertEqual(findings_for(ai_bom(TODAY.isoformat() + "T00:00:00Z")), [])

    def test_stale_date_reports_its_real_age(self):
        found = findings_for(ai_bom((TODAY - timedelta(days=200)).isoformat()))
        self.assertEqual(len(found), 1)
        self.assertIn("200 days old", found[0])

    def test_absent_field_reports_missing(self):
        found = findings_for(ai_bom())
        self.assertEqual(len(found), 1)
        self.assertIn("missing or unparsable", found[0])

    def test_root_level_value_does_not_satisfy_the_check(self):
        instance = ai_bom()
        instance["last_reviewed"] = TODAY.isoformat()
        found = findings_for(instance)
        self.assertEqual(len(found), 1)
        self.assertIn("missing or unparsable", found[0])


class ShippedTemplate(unittest.TestCase):
    def test_the_shipped_ai_bom_field_is_found_and_parsed(self):
        """Whatever its age, the template's own field must reach the check."""
        import yaml

        with (REPO_ROOT / "templates" / "ai-bom.yaml").open() as f:
            instance = yaml.safe_load(f)
        for finding in findings_for(instance):
            self.assertNotIn("missing or unparsable", finding)


if __name__ == "__main__":
    unittest.main()
