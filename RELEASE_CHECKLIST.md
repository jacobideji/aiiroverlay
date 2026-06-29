<!-- ────────────────────────────────────────────────────────────────── -->
<!--  Release Checklist                                                 -->
<!--  Part of the AI IR Overlay™ framework, by Jacob Ideji              -->
<!--  https://jacobideji.com                                            -->
<!--  License: Apache 2.0. See LICENSE file in this package.            -->
<!-- ────────────────────────────────────────────────────────────────── -->

# Release Checklist

> *Run this checklist before tagging any release. Each step prevents a real defect that surfaced in a prior cycle.*

This checklist exists because release hygiene has historically been the framework's weakest link. Three release tags (v0.12.0, v0.13.0, v0.14.0) were not cut despite CHANGELOG entries, and `CITATION.cff` has gone stale on two consecutive releases. This checklist closes those gaps.

## Pre-flight (must complete before `git push`)

- [ ] `CHANGELOG.md` has a new `[X.Y.Z] · YYYY-MM-DD · Title` entry with `### Added` / `### Changed` / `### Why now` sections.
- [ ] `CHANGELOG.md` `[Unreleased]` link reference at the bottom of the file is bumped to compare from `vX.Y.Z...HEAD`.
- [ ] `CHANGELOG.md` adds a new `[X.Y.Z]: https://github.com/jacobideji/aiiroverlay/releases/tag/vX.Y.Z` link reference.
- [ ] `CITATION.cff` `version:` field bumped to `"X.Y.Z"`.
- [ ] `CITATION.cff` `preferred-citation.version:` field bumped to `"X.Y.Z"`.
- [ ] `CITATION.cff` `date-released:` field set to the release date.
- [ ] `SECURITY.md` Supported Versions table reflects the new latest minor and (if a MINOR bump) previous-minor cutoff.
- [ ] `CONTENT_MAP.md` Status column updated for any artifact whose status changed in this release.
- [ ] If any new file is added under `templates/`, `schemas/`, or `scripts/validate.py`: the change touches a path that triggers `.github/workflows/validate-templates.yml`. This forces the workflow to fire on the release commit so the Actions tab shows a green run.
- [ ] If the release is hygiene-only (no template/schema/script changes): manually dispatch the validate-templates workflow via the Actions tab so this release has a green CI run.

## Post-push (must complete after `git push`)

- [ ] Cut the GitHub release tag: `gh release create vX.Y.Z --title "vX.Y.Z: <Title>" --notes-file <(awk '/^## \[X.Y.Z\]/,/^## \[/' CHANGELOG.md | head -n -2)`.
- [ ] Open the GitHub Actions tab. Confirm the `Validate templates against schemas` workflow has a green run on the release commit.
- [ ] Open the CHANGELOG link reference (`[X.Y.Z]: ...`) in a browser. Confirm it resolves to HTTP 200.
- [ ] Open `https://aiir.jacobideji.com/schemas/ai-bom.schema.json`. Confirm it serves the latest schema content.

## Backfill (one-time, applies to historical releases that pre-date this checklist)

These tags exist in `CHANGELOG.md` link references but have not been cut on GitHub. Backfill them by tagging the appropriate historical main-branch commit:

- [ ] `v0.12.0` (Playbook 06 + Materiality and Disclosure)
- [ ] `v0.13.0` (Playbook 10: Vendor Copilots)
- [ ] `v0.14.0` (Schemas Directory)

Backfill command pattern (substitute the actual commit SHA from `git log --oneline` for each release commit):

```bash
gh release create v0.12.0 --target <commit-sha> \
  --title "v0.12.0: Playbook 06 + Materiality and Disclosure" \
  --notes-file <(awk '/^## \[0.12.0\]/,/^## \[/' CHANGELOG.md | head -n -2)
```

Repeat for `v0.13.0` and `v0.14.0`. Once backfilled, every CHANGELOG link reference resolves to HTTP 200.

## Why this checklist exists

Three release-hygiene defects surfaced in the v0.14.1 calibration review:

1. **CITATION.cff stale.** After v0.14.1 shipped, `CITATION.cff` still pinned `version: "0.14.0"`. Anyone citing the framework academically would cite a stale version.
2. **Broken CHANGELOG link refs.** Three release tags (v0.12.0, v0.13.0, v0.14.0) were never cut on GitHub. Clicking those CHANGELOG entries returned HTTP 404.
3. **Workflow never ran.** The `validate-templates.yml` workflow's `push` trigger did not include its own path, so its installation commit did not fire the workflow. The Actions tab showed zero validator runs.

This checklist surfaces each of those concerns as a step the maintainer must check off before declaring a release shipped.

---

*Source: AI IR Overlay framework, maintainer's release hygiene discipline, by Jacob Ideji.*
<https://www.linkedin.com/in/jacobideji/>
