#!/usr/bin/env python3
"""Repository consistency checks for the AI IR Overlay.

`scripts/validate.py` checks the framework's *data* against its schemas. This
checks the repository's *claims* against each other, which is the class of
defect that every release from v0.37.0 to v0.43.0 had to correct one at a
time. Each check below exists because a specific defect reached a published
release; the docstring on each names it.

What this cannot check: whether the incident-response guidance is correct as
practice, whether any external organization has run the Offensive Lens, and
the contents of the lens fixture and assessment records, which
`offensive-lens/VALIDATION.md` states are maintained with the lens source
rather than here. Those are judgements and off-repo artifacts; no script
closes them, and a green run here does not claim they are closed.

Usage
-----
    python3 scripts/check_repo.py            # all checks
    python3 scripts/check_repo.py --list     # names only

Exit codes
----------
    0  every check passed
    1  one or more checks failed
    2  usage error
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", "__pycache__", "node_modules"}
WORKFLOW = REPO_ROOT / ".github" / "workflows" / "validate-templates.yml"


# ─── helpers ──────────────────────────────────────────────────────────────

def walk(suffixes: tuple[str, ...]) -> list[Path]:
    out: list[Path] = []
    for root, dirs, files in os.walk(REPO_ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if f.endswith(suffixes):
                out.append(Path(root) / f)
    return sorted(out)


def rel(p: Path) -> str:
    return str(p.relative_to(REPO_ROOT))


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


def prose(text: str) -> str:
    """Markdown with fenced blocks and inline code removed."""
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    return re.sub(r"`[^`\n]*`", "", text)


def slug(heading: str) -> str:
    h = re.sub(r"`", "", heading)
    h = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", h)
    h = re.sub(r"[^\w\s-]", "", h.strip().lower(), flags=re.U)
    return h.replace(" ", "-")


def anchors_of(p: Path) -> set[str]:
    found: set[str] = set()
    fence = False
    for line in read(p).split("\n"):
        if line.lstrip().startswith("```"):
            fence = not fence
            continue
        if fence:
            continue
        m = re.match(r"^#{1,6}\s+(.*)$", line.rstrip())
        if not m:
            continue
        base = s = slug(m.group(1))
        n = 1
        while s in found:
            s = f"{base}-{n}"
            n += 1
        found.add(s)
    return found


LINK = re.compile(r"(?<!!)\[(?:[^\]\[]|\[[^\]]*\])*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")


# ─── checks ───────────────────────────────────────────────────────────────

def check_links() -> list[str]:
    """Relative links and in-page anchors resolve.

    v0.39.0 shipped a MATRIX replacement that dropped a CONTRIBUTING link;
    v0.38.0 fixed a MATRIX link that pointed at a bare directory.
    """
    md = walk((".md",))
    anchors = {rel(p): anchors_of(p) for p in md}
    bad: list[str] = []
    for p in md:
        here = rel(p)
        for m in LINK.finditer(prose(read(p))):
            target = m.group(1)
            if target.startswith(("http://", "https://", "mailto:", "tel:")):
                continue
            path, _, frag = target.partition("#")
            if not path:
                if frag and frag not in anchors[here]:
                    bad.append(f"{here}: anchor #{frag} does not exist in this file")
                continue
            resolved = os.path.normpath(os.path.join(os.path.dirname(here), path))
            if not (REPO_ROOT / resolved).exists():
                bad.append(f"{here}: link target {target} does not exist")
            elif frag and resolved in anchors and frag not in anchors[resolved]:
                bad.append(f"{here}: anchor #{frag} does not exist in {resolved}")
    return bad


def check_whitespace() -> list[str]:
    """No trailing whitespace, CRLF line endings, or tabs in markdown.

    v0.39.2 corrected four lines of trailing whitespace; `SECURITY.md` names
    markdownlint-cli2 as repository tooling and MD009 flags exactly this.
    """
    bad: list[str] = []
    for p in walk((".md",)):
        raw = p.read_bytes()
        if b"\r\n" in raw:
            bad.append(f"{rel(p)}: CRLF line endings")
        text = raw.decode("utf-8", "replace")
        if "\t" in text:
            bad.append(f"{rel(p)}: contains a tab")
        for i, line in enumerate(text.split("\n"), 1):
            if line != line.rstrip():
                bad.append(f"{rel(p)}:{i}: trailing whitespace")
    return bad


def check_tables() -> list[str]:
    """Every markdown table row has the same cell count as its header."""
    bad: list[str] = []
    for p in walk((".md",)):
        lines = read(p).split("\n")
        fence = False
        i = 0
        while i < len(lines):
            if lines[i].lstrip().startswith("```"):
                fence = not fence
                i += 1
                continue
            if fence:
                i += 1
                continue
            is_table = (
                lines[i].startswith("|")
                and i + 1 < len(lines)
                and re.match(r"^\|[\s:|-]+\|?\s*$", lines[i + 1])
            )
            if not is_table:
                i += 1
                continue
            width = len(lines[i].strip("|").split("|"))
            j = i + 2
            while j < len(lines) and lines[j].startswith("|"):
                got = len(lines[j].strip("|").split("|"))
                if got != width:
                    bad.append(f"{rel(p)}:{j + 1}: header has {width} cells, row has {got}")
                j += 1
            i = j
    return bad


def check_identifiers() -> list[str]:
    """Every PB and OL-T identifier cited anywhere resolves to a real one.

    PB25 is exempt: `crosswalks/owasp-agentic-top-10.md` names it explicitly
    as a v1.1 candidate rather than an existing playbook.
    """
    playbooks = {
        "PB" + p.name[:2]
        for p in (REPO_ROOT / "playbooks").glob("*.md")
        if re.match(r"\d\d-", p.name)
    }
    lens_matrix = REPO_ROOT / "offensive-lens" / "MATRIX.md"
    techniques = set(re.findall(r"OL-T\d{3}", read(lens_matrix)))
    exempt = {"PB25"}
    bad: list[str] = []
    for p in walk((".md",)):
        if p.name == "CHANGELOG.md":
            continue
        text = read(p)
        for ident in sorted(set(re.findall(r"\bPB\d{2}\b", text)) - playbooks - exempt):
            bad.append(f"{rel(p)}: cites {ident}, which is not a playbook in playbooks/")
        for ident in sorted(set(re.findall(r"OL-T\d{3}", text)) - techniques):
            bad.append(f"{rel(p)}: cites {ident}, which is not in offensive-lens/MATRIX.md")
    return bad


def check_changelog_ledger() -> list[str]:
    """Every release entry has a link reference, and each URL is well formed.

    v0.41.0 and v0.42.0 both shipped without their own link reference, so the
    two newest headings rendered as plain text; v0.42.1 found it and also
    found `[Unreleased]` two releases behind. v0.42.1 removed a reference URL
    carrying a literal trailing comma.
    """
    text = read(REPO_ROOT / "CHANGELOG.md")
    entries = [
        m.group(1)
        for m in re.finditer(r"^## \[([^\]]+)\]", text, re.M)
        if m.group(1).lower() != "unreleased"
    ]
    refs = dict(re.findall(r"^\[([^\]]+)\]:\s*(\S+)$", text, re.M))
    bad: list[str] = []
    for version in entries:
        if version not in refs:
            bad.append(f"CHANGELOG.md: entry [{version}] has no link reference")
    for name, url in refs.items():
        if name == "Unreleased":
            continue
        if url != f"https://github.com/jacobideji/aiiroverlay/releases/tag/v{name}":
            bad.append(f"CHANGELOG.md: reference [{name}] has an unexpected URL: {url}")
    unreleased = refs.get("Unreleased", "")
    if entries:
        expected = f"https://github.com/jacobideji/aiiroverlay/compare/v{entries[0]}...HEAD"
        if unreleased != expected:
            bad.append(
                f"CHANGELOG.md: [Unreleased] should compare from v{entries[0]}, got {unreleased}"
            )
    return bad


def check_workflow_paths() -> list[str]:
    """Prose describing the CI trigger paths matches the workflow's own paths.

    v0.43.0 added `tests/**` to the triggers and left `CONTENT_MAP.md` and
    `RELEASE_CHECKLIST.md` describing the previous set.
    """
    if not WORKFLOW.exists():
        return [f"{rel(WORKFLOW)}: missing"]
    declared = set(re.findall(r'^\s*-\s*"([^"]+)"\s*$', read(WORKFLOW), re.M))
    declared = {d for d in declared if "/" in d or d.endswith(".py")}
    watched = {d for d in declared if not d.startswith(".github/")}

    def stem(path: str) -> str:
        """`templates/**`, `templates/` and `templates` all name one path."""
        return path.rstrip("*").rstrip("/")

    bad: list[str] = []
    for name in ("CONTENT_MAP.md", "RELEASE_CHECKLIST.md"):
        text = read(REPO_ROOT / name)
        for line_no, line in enumerate(text.split("\n"), 1):
            if "validate-templates" not in line and "triggers" not in line:
                continue
            named = {stem(x) for x in re.findall(r"`([^`]+)`", line)}
            if not named & {stem(w) for w in watched}:
                continue
            missing = sorted(w for w in watched if stem(w) not in named)
            if missing:
                bad.append(
                    f"{name}:{line_no}: names CI trigger paths but omits {missing}"
                )
    return bad


def check_demo_modes() -> list[str]:
    """Prose describing the kill-switch demo names the modes it implements.

    v0.41.0 corrected three documents that said the demo covered M0-M4 and
    missed a fourth in `CONTENT_MAP.md`, which still said M0/M1/M2/M3/M4
    while the code implemented M0 through M5.
    """
    demo = REPO_ROOT / "reference-impls" / "kill_switch_demo" / "kill_switch_demo.py"
    if not demo.exists():
        return [f"{rel(demo)}: missing"]
    m = re.search(r"^ALL_MODES\s*=\s*\[([^\]]+)\]", read(demo), re.M)
    if not m:
        return [f"{rel(demo)}: ALL_MODES not found"]
    implemented = sorted(set(re.findall(r"M\d", m.group(1))))
    highest = implemented[-1]
    bad: list[str] = []
    for p in walk((".md",)):
        if p.name == "CHANGELOG.md" or "offensive-lens" in rel(p):
            continue
        for line_no, line in enumerate(read(p).split("\n"), 1):
            if "kill_switch_demo" not in line and "Kill-Switch Demo" not in line:
                continue
            listed = re.findall(r"M\d(?:[/,]\s*M\d)+", line)
            for run in listed:
                names = sorted(set(re.findall(r"M\d", run)))
                if names and names[-1] != highest:
                    bad.append(
                        f"{rel(p)}:{line_no}: describes the demo as {run} "
                        f"but it implements through {highest}"
                    )
    return bad


def check_validator_field_paths() -> list[str]:
    """Nested paths the validator reads exist in the shipped AI-BOM.

    v0.43.0 fixed a read of `last_reviewed` from the document root when the
    schema places it at `agent.last_reviewed`, so the 7-day Inventory
    Currency check never evaluated.
    """
    try:
        import yaml
    except ImportError:
        return ["pyyaml not installed; cannot check validator field paths"]
    source = read(REPO_ROOT / "scripts" / "validate.py")
    instance = yaml.safe_load((REPO_ROOT / "templates" / "ai-bom.yaml").read_text())
    bad: list[str] = []
    pattern = re.compile(
        r'\(?instance\.get\("(?P<outer>\w+)"\)(?:\s*or\s*\{\})?\)?\.get\("(?P<inner>\w+)"\)'
    )
    for m in pattern.finditer(source):
        outer, inner = m.group("outer"), m.group("inner")
        container = instance.get(outer)
        if not isinstance(container, dict) or inner not in container:
            bad.append(
                f"scripts/validate.py: reads {outer}.{inner}, "
                f"absent from templates/ai-bom.yaml"
            )
    for m in re.finditer(r'instance\.get\("(\w+)"\)(?!\s*or\s*\{\})(?!\.get)', source):
        key = m.group(1)
        if key not in instance:
            bad.append(
                f"scripts/validate.py: reads top-level {key}, "
                f"absent from templates/ai-bom.yaml"
            )
    return bad


def check_tooling_is_mapped() -> list[str]:
    """Every shipped script and test appears in CONTENT_MAP.md.

    v0.43.0 added `tests/test_validate.py` without a CONTENT_MAP row, in a
    table that already rows the validator, the CI workflow and both
    reference implementations.
    """
    mapped = read(REPO_ROOT / "CONTENT_MAP.md")
    bad: list[str] = []
    for d in ("scripts", "tests"):
        folder = REPO_ROOT / d
        if not folder.is_dir():
            continue
        for p in sorted(folder.glob("*.py")):
            if rel(p) not in mapped:
                bad.append(f"CONTENT_MAP.md: no row for {rel(p)}")
    return bad


def check_tree_blocks() -> list[str]:
    """Fenced directory trees list only paths that exist.

    `offensive-lens/README.md` shipped a tree naming `offensive-lens/` and
    `dist/`, which are artifacts of the lens's authoring workspace rather
    than this repository, while omitting `FINDINGS.md`, which the same
    file's reading order lists as item 5.
    """
    entry_re = re.compile(r"^([A-Za-z0-9_.-]+(?:/|\.md|\.py|\.json|\.ya?ml|\.csv|\.cff))\s")
    bad: list[str] = []
    for p in walk((".md",)):
        text = read(p)
        for block in re.findall(r"```[a-z]*\n(.*?)```", text, re.S):
            entries = [m.group(1) for m in (entry_re.match(l) for l in block.split("\n")) if m]
            if len(entries) < 3:
                continue  # not a directory listing
            for entry in entries:
                target = os.path.normpath(
                    os.path.join(os.path.dirname(p), entry.rstrip("/"))
                )
                if not Path(target).exists():
                    bad.append(f"{rel(p)}: tree lists {entry}, which does not exist")
    return bad


def check_composition_counts() -> list[str]:
    """A sentence claiming the full framework's composition counts correctly.

    `QUICKSTART-startup.md` said the framework has three crosswalks; v0.40.0
    added `crosswalks/sp-800-61r3.md` as the fourth and updated README,
    MATRIX and CONTENT_MAP but not this sentence.

    Deliberately narrow: only sentences introduced by "full framework has"
    are checked, because the repository also states counts for the startup
    subset, and those are smaller by design.
    """
    counters = {
        "playbooks": lambda: len(
            [p for p in (REPO_ROOT / "playbooks").glob("*.md") if re.match(r"\d\d-", p.name)]
        ),
        "framework foundation docs": lambda: len(list((REPO_ROOT / "framework").glob("*.md"))),
        "schemas": lambda: len(list((REPO_ROOT / "schemas").iterdir())),
        "crosswalks": lambda: len(list((REPO_ROOT / "crosswalks").glob("*.md"))),
    }
    bad: list[str] = []
    for p in walk((".md",)):
        if p.name == "CHANGELOG.md":
            continue
        for sentence in re.findall(r"full framework has ([^.]+)\.", read(p)):
            for noun, count in counters.items():
                m = re.search(r"(\d+)\s+" + re.escape(noun), sentence)
                if m and int(m.group(1)) != count():
                    bad.append(
                        f"{rel(p)}: claims {m.group(1)} {noun}, repository has {count()}"
                    )
    return bad


CHECKS = [
    ("relative links and anchors resolve", check_links),
    ("no trailing whitespace, CRLF or tabs", check_whitespace),
    ("markdown tables are rectangular", check_tables),
    ("PB and OL-T identifiers resolve", check_identifiers),
    ("changelog entries and link references agree", check_changelog_ledger),
    ("CI trigger paths described accurately", check_workflow_paths),
    ("demo mode coverage described accurately", check_demo_modes),
    ("validator field paths exist in the AI-BOM", check_validator_field_paths),
    ("shipped scripts and tests appear in CONTENT_MAP", check_tooling_is_mapped),
    ("directory trees list paths that exist", check_tree_blocks),
    ("stated composition counts are correct", check_composition_counts),
]


def main(argv: list[str]) -> int:
    if argv and argv[0] not in ("--list",):
        print(f"usage: {Path(__file__).name} [--list]", file=sys.stderr)
        return 2
    if argv == ["--list"]:
        for name, fn in CHECKS:
            print(f"{name}\n    {(fn.__doc__ or '').strip().splitlines()[0]}")
        return 0

    print("AI IR Overlay repository checks\n")
    total = 0
    for name, fn in CHECKS:
        failures = fn()
        total += len(failures)
        print(f"{'FAIL' if failures else 'ok  '}  {name}")
        for f in failures:
            print(f"        {f}")
    print()
    if total:
        print(f"{total} finding(s). This script checks claims against each other;")
        print("it does not check whether the guidance is correct as practice.")
        return 1
    print("All checks passed. Judgement items remain out of scope: see the")
    print("module docstring for what this script does not check.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
