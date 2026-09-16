#!/usr/bin/env python3
"""Algorithmic conformance checker for note-format-spec.md (v2.0.0).

Checks the mechanically decidable rules of note-format-spec.md and reports
violations citing rule IDs. Judgment clauses — whether a Summary is
*accurate* (R8's SHOULD), whether a repair preserved the user's meaning
(O2) — are out of scope; see note-set-operations.md for the split.

Usage (run from the top of the note-set repository):
    python3 check_notes.py <note.md> [<note.md> ...]   # R1-R5, R7, R8
    python3 check_notes.py --all                       # notes/ plus R6

Exit codes: 0 all conformant; 1 violations found; 2 usage or I/O error.
"""

import os
import re
import sys
from datetime import date

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
# R6 entry form: "- [Title](notes/<slug>.md) — <first sentence of Summary>"
INDEX_ENTRY_RE = re.compile(r"^- \[(?P<title>.+?)\]\((?P<path>[^)]+)\) — (?P<summary>.+)$")

NOTES_DIR = "notes"
INDEX_FILE = "index.md"


def slug(title):
    """R7: lowercase, drop apostrophes, non-alphanumeric runs -> one hyphen."""
    s = title.lower().replace("'", "").replace("’", "")
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def read_lines(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read().splitlines()
    except OSError as exc:
        print(f"error: cannot read {path}: {exc}", file=sys.stderr)
        sys.exit(2)


def parse_note(path):
    """Split a note into (fields, body, r1_problems). fields is None on R1 failure."""
    lines = read_lines(path)
    if not lines or lines[0] != "---":
        return None, lines, ["the opening '---' fence is not the first line of the file"]
    close = next((i for i in range(1, len(lines)) if lines[i] == "---"), None)
    if close is None:
        return None, lines[1:], ["the front-matter block is never closed by a '---' fence"]
    return lines[1:close], lines[close + 1:], []


def headings_of(body):
    """All headings as (line_index, level, text), skipping fenced code blocks."""
    result, in_fence = [], False
    for idx, line in enumerate(body):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = HEADING_RE.match(line)
        if m:
            result.append((idx, len(m.group(1)), m.group(2)))
    return result


def summary_paragraphs(body, headings):
    """Paragraph blocks inside the '## Summary' section, or None if absent."""
    sections = [h for h in headings if h[1] >= 2]
    if not sections or sections[0][1] != 2 or sections[0][2] != "Summary":
        return None
    start = sections[0][0] + 1
    end = next((idx for idx, _, _ in headings if idx > sections[0][0]), len(body))
    paragraphs, current = [], []
    for line in body[start:end]:
        if line.strip():
            current.append(line.strip())
        elif current:
            paragraphs.append(" ".join(current))
            current = []
    if current:
        paragraphs.append(" ".join(current))
    return paragraphs


def first_sentence(paragraph):
    text = " ".join(paragraph.split())
    m = re.search(r"\.(\s|$)", text)
    return text[: m.end()].strip() if m else text


def check_note(path, findings):
    def report(rule, message):
        findings.append(f"{path}: {rule}: {message}")

    fields_lines, body, r1_problems = parse_note(path)
    for problem in r1_problems:
        report("R1", problem)

    # R2 — exactly `title` and `created`, created a valid ISO-8601 date.
    title = None
    if fields_lines is not None:
        fields = {}
        for line in fields_lines:
            if not line.strip():
                continue
            key, sep, value = line.partition(":")
            if not sep or not key.strip():
                report("R2", f"front-matter line is not a 'key: value' field: {line!r}")
                continue
            key = key.strip()
            if key in fields:
                report("R2", f"duplicate front-matter field '{key}'")
            fields[key] = value.strip()
        for extra in sorted(set(fields) - {"title", "created"}):
            report("R2", f"unexpected front-matter field '{extra}'")
        title = fields.get("title")
        if not title:
            report("R2", "front-matter field 'title' is missing or empty")
            title = None
        created = fields.get("created")
        if created is None:
            report("R2", "front-matter field 'created' is missing")
        elif not DATE_RE.match(created):
            report("R2", f"created date {created!r} is not ISO-8601 (YYYY-MM-DD)")
        else:
            try:
                date.fromisoformat(created)
            except ValueError:
                report("R2", f"created date {created!r} is not a valid calendar date")

    headings = headings_of(body)

    # R3 — body begins with an H1 whose text equals the front-matter title.
    first_nonblank = next((i for i, line in enumerate(body) if line.strip()), None)
    if first_nonblank is None:
        report("R3", "note body is empty; it must begin with a level-1 heading")
    else:
        m = HEADING_RE.match(body[first_nonblank])
        if not m or len(m.group(1)) != 1:
            report("R3", "the first non-blank line of the body is not a level-1 heading")
        elif title is not None and m.group(2) != title:
            report("R3", f"H1 {m.group(2)!r} does not match front-matter title {title!r}")

    # R4 — exactly one H1.
    h1_count = sum(1 for _, level, _ in headings if level == 1)
    if h1_count > 1:
        report("R4", f"found {h1_count} level-1 headings; exactly one is allowed")

    # R5 — no skipped heading levels.
    previous_level = None
    for _, level, text in headings:
        if previous_level is not None and level > previous_level + 1:
            report("R5", f"heading {'#' * level + ' ' + text!r} skips from level "
                         f"{previous_level} to level {level}")
        previous_level = level

    # R7 — filename is the slug of the title.
    if title is not None:
        expected = slug(title) + ".md"
        if os.path.basename(path) != expected:
            report("R7", f"filename {os.path.basename(path)!r} does not match the "
                         f"slug of the title (expected {expected!r})")

    # R8 — first section is '## Summary' with exactly one paragraph.
    paragraphs = summary_paragraphs(body, headings)
    if paragraphs is None:
        report("R8", "the first section heading must be '## Summary'")
    elif len(paragraphs) != 1:
        report("R8", f"the Summary section must contain exactly one paragraph "
                     f"(found {len(paragraphs)})")


def check_index(findings):
    if not os.path.isdir(NOTES_DIR):
        print(f"error: no {NOTES_DIR}/ directory here; run from the repository top",
              file=sys.stderr)
        sys.exit(2)
    if not os.path.isfile(INDEX_FILE):
        print(f"error: {INDEX_FILE} not found; run from the repository top",
              file=sys.stderr)
        sys.exit(2)

    def report(message):
        findings.append(f"{INDEX_FILE}: R6: {message}")

    note_files = sorted(
        os.path.join(NOTES_DIR, name)
        for name in os.listdir(NOTES_DIR)
        if name.endswith(".md")
    )

    linked = {}
    for line in read_lines(INDEX_FILE):
        if not line.startswith("- ["):
            continue
        m = INDEX_ENTRY_RE.match(line)
        if not m:
            report(f"entry is not in the required form "
                   f"'- [Title](notes/<slug>.md) — <summary sentence>': {line!r}")
            continue
        target = m.group("path")
        linked[target] = linked.get(target, 0) + 1
        if not os.path.isfile(target):
            report(f"entry links to a missing file: {target}")
            continue
        _, body, _ = parse_note(target)
        paragraphs = summary_paragraphs(body, headings_of(body))
        if paragraphs:
            expected = first_sentence(paragraphs[0])
            actual = " ".join(m.group("summary").split())
            if actual != expected:
                report(f"entry text for {target} does not match the first sentence "
                       f"of its Summary (expected {expected!r})")

    for target, count in sorted(linked.items()):
        if count > 1:
            report(f"{target} is linked {count} times; exactly once is required")
    for path in note_files:
        if path not in linked:
            report(f"{path} is not linked from {INDEX_FILE}")

    return note_files


def main(argv):
    if not argv or (len(argv) > 1 and "--all" in argv):
        print("usage: python3 check_notes.py <note.md> [<note.md> ...] | --all",
              file=sys.stderr)
        return 2

    findings = []
    if argv == ["--all"]:
        note_files = check_index(findings)
        for path in note_files:
            check_note(path, findings)
        checked = f"{len(note_files)} note(s) and {INDEX_FILE}"
    else:
        for path in argv:
            if not os.path.isfile(path):
                print(f"error: no such file: {path}", file=sys.stderr)
                return 2
        for path in argv:
            check_note(path, findings)
        checked = f"{len(argv)} file(s)"

    for finding in findings:
        print(finding)
    if findings:
        print(f"Checked {checked}: {len(findings)} violation(s).")
        return 1
    print(f"Checked {checked}: all conformant.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
