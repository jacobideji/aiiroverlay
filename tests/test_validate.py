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


def level_4(history=None):
    """A Level 4 instance, current on every m1-m4 record."""
    modes = {
        k: {"implemented": True, "tested_at": TODAY.isoformat(), "tta_minutes": 1}
        for k in ("m1_read_only", "m2_approvals", "m3_tool_tiering", "m4_full_disable")
    }
    return {
        "agent": {"last_reviewed": TODAY.isoformat()},
        "kill_switches": dict(maturity_target="level_4_resilient", **modes),
        "incidents_history": [] if history is None else history,
    }


def m5_findings(instance):
    return [
        f
        for f in validate.check_staleness(instance, today=TODAY)
        if "incidents_history" in f
    ]


class LevelFourRequiresAnM5Drill(unittest.TestCase):
    """M5 carries no kill_switches record by design; its drills live in
    incidents_history, which the validator did not read before v0.45.0."""

    def test_no_m5_record_is_a_finding(self):
        found = m5_findings(level_4())
        self.assertEqual(len(found), 1)
        self.assertIn("no M5 Controlled Re-Enable record", found[0])

    def test_stale_m5_drill_reports_its_age(self):
        old = (TODAY - timedelta(days=200)).isoformat()
        found = m5_findings(level_4([{"date": old, "mode_activated": "M5"}]))
        self.assertEqual(len(found), 1)
        self.assertIn("200 days old", found[0])

    def test_recent_m5_drill_is_clean(self):
        now = TODAY.isoformat()
        self.assertEqual(m5_findings(level_4([{"date": now, "mode_activated": "M5"}])), [])

    def test_a_non_m5_drill_does_not_satisfy_it(self):
        now = TODAY.isoformat()
        found = m5_findings(level_4([{"date": now, "mode_activated": "M1"}]))
        self.assertEqual(len(found), 1)
        self.assertIn("no M5 Controlled Re-Enable record", found[0])

    def test_an_unparsable_m5_date_is_reported_not_raised(self):
        """The first draft of this gate raised ValueError on this input."""
        found = m5_findings(level_4([{"date": "not-a-date", "mode_activated": "M5"}]))
        self.assertEqual(len(found), 1)
        self.assertIn("missing or unparsable", found[0])

    def test_lower_levels_are_not_asked_for_an_m5_drill(self):
        inst = level_4()
        inst["kill_switches"]["maturity_target"] = "level_2_containable"
        self.assertEqual(m5_findings(inst), [])


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
