"""Validate Badil's reference portfolio; no AI calls or network access."""

import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
errors = []
checks = 0


def check(condition, message):
    global checks
    checks += 1
    if not condition:
        errors.append(message)


def read_json(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def validate():
    required = [
        "README.md", "CHANGELOG.md", "CONTRIBUTING.md",
        "01-prompt-engineering/prompt-library.md",
        "01-prompt-engineering/before-after-example.md",
        "02-writing-workflow/professional-writing-example.md",
        "03-information-workflow/information-processing-example.md",
        "04-planning-workflow/planning-example.md",
        "05-verification/verification-checklist.md",
        "05-verification/review-log.md",
        "06-responsible-ai/responsible-use-checklist.md",
        "07-integration-plan/personal-integration-plan.md",
        "docs/technical-documentation.md", "docs/training-program.md",
        "docs/project-metadata.json", "outputs/evidence-map.md",
    ]
    for path in required:
        check((ROOT / path).is_file(), f"Missing required file: {path}")

    sources = read_json("examples/sources.json")
    tasks = read_json("outputs/tasks.json")
    check(isinstance(sources, list), "Sources must be an array")
    check(isinstance(tasks, list), "Tasks must be an array")
    if not isinstance(sources, list) or not isinstance(tasks, list):
        return
    source_fields = {"id", "timestamp", "timezone", "role", "text"}
    for source in sources:
        valid = (isinstance(source, dict) and set(source) == source_fields
                 and all(isinstance(value, str) and value.strip() for value in source.values()))
        check(valid, "Source fields must be complete non-empty strings")
        if not valid:
            return
    fields = {"id", "task", "owner", "due_date", "due_text", "status", "sources",
              "dependency", "priority", "priority_reason"}
    for task in tasks:
        valid = isinstance(task, dict) and set(task) == fields
        check(valid, "Unexpected task fields")
        if not valid:
            return
        for field in ("id", "task", "due_text", "status", "priority", "priority_reason"):
            valid = isinstance(task[field], str) and bool(task[field].strip())
            check(valid, f"Task field must be a non-empty string: {field}")
            if not valid:
                return
        for field in ("owner", "due_date", "dependency"):
            valid = task[field] is None or (isinstance(task[field], str) and bool(task[field].strip()))
            check(valid, f"Invalid nullable field: {task['id']}.{field}")
            if not valid:
                return
        valid = (isinstance(task["sources"], list) and bool(task["sources"])
                 and all(isinstance(item, str) and item for item in task["sources"]))
        check(valid, f"Evidence must be a non-empty array of IDs: {task['id']}")
        if not valid:
            return
        check(len(task["sources"]) == len(set(task["sources"])), f"Repeated evidence: {task['id']}")
        check(task["priority"] in {"عالية", "تحتاج تقييمًا"}, f"Unknown priority: {task['id']}")
    source_ids = [s["id"] for s in sources]
    task_ids = [t["id"] for t in tasks]
    check(len(source_ids) == len(set(source_ids)), "Duplicate source IDs")
    check(len(task_ids) == len(set(task_ids)), "Duplicate task IDs")
    check(set(source_ids) == {f"M{i:02}" for i in range(1, 16)} | {"N01"},
          "Reference scenario requires 15 messages and one meeting")
    check(set(task_ids) == {f"T{i:02}" for i in range(1, 9)},
          "Reference scenario requires eight main tasks")
    raw = (ROOT / "examples/raw-input.md").read_text(encoding="utf-8")
    for source in sources:
        marker = "## " + source["id"] + "\n"
        check(raw.count(marker) == 1, f"Missing/duplicate Markdown source {source['id']}")
        section = raw.split(marker, 1)[-1].split("\n## ", 1)[0]
        for field in ("text", "role", "timestamp"):
            check(source[field] in section,
                  f"Source Markdown/JSON mismatch: {source['id']}.{field}")
        datetime.strptime(source["timestamp"], "%Y-%m-%d %H:%M")
        check(source["timezone"] == "Asia/Riyadh", "Unexpected scenario timezone")

    handover = (ROOT / "outputs/handover.md").read_text(encoding="utf-8")
    for task in tasks:
        check(set(task) == fields, f"Unexpected fields in {task['id']}")
        check(isinstance(task["sources"], list) and bool(task["sources"]),
              f"Missing evidence in {task['id']}")
        check(set(task["sources"]) <= set(source_ids), f"Unknown evidence in {task['id']}")
        for field in ("owner", "dependency"):
            check(task[field] is None or isinstance(task[field], str),
                  f"Invalid nullable field {task['id']}.{field}")
        if task["due_date"] is not None:
            check(bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", task["due_date"])),
                  f"Invalid date format in {task['id']}")
            date.fromisoformat(task["due_date"])
        rows = [row for row in handover.splitlines()
                if row.startswith(f"| {task['id']} |") and len(row.strip("|").split("|")) == 6]
        check(len(rows) == 1, f"Missing/duplicate handover row: {task['id']}")
        if rows:
            cells = [cell.strip() for cell in rows[0].strip("|").split("|")]
            expected = [task["id"], task["task"], task["owner"] or "غير محدد",
                        task["due_text"], task["status"]]
            check(cells[:5] == expected, f"Handover/JSON facts differ: {task['id']}")
            for source_id in task["sources"]:
                check(f"[{source_id}]" in rows[0], f"Missing visible evidence {task['id']}/{source_id}")
        priority_row = f"| {task['id']} | {task['priority']} | {task['priority_reason']} |"
        check(priority_row in handover, f"Visible priority differs from JSON: {task['id']}")

    # Scenario-specific regression checks guard high-impact inference mistakes.
    by_id = {t["id"]: t for t in tasks}
    known = {"T01": ("سارة", "2026-10-04"), "T03": ("سارة", "2026-10-05"),
             "T05": ("يوسف", "2026-10-08"), "T08": ("عمر", "2026-10-08")}
    for tid, (owner, deadline) in known.items():
        check(by_id[tid]["owner"] == owner, f"Known owner changed: {tid}")
        check(by_id[tid]["due_date"] == deadline and by_id[tid]["due_text"] == deadline,
              f"Known deadline changed: {tid}")
    for tid in ("T02", "T07"):
        check(by_id[tid]["due_date"] is None and by_id[tid]["due_text"] == "غير محدد",
              f"Unknown deadline invented: {tid}")
    for tid in ("T02", "T04", "T06", "T07"):
        check(by_id[tid]["owner"] is None, f"Unsupported owner filled for {tid}")
    check(by_id["T04"]["due_date"] is None, "Conflicting delivery date was resolved without evidence")
    check(all(d in by_id["T04"]["due_text"] for d in ("2026-10-06", "2026-10-07")),
          "Both conflicting dates must remain visible")
    check(by_id["T06"]["due_date"] is None, "Relative access deadline must not become an invented exact date")
    check(by_id["T06"]["status"] == "غير مفعلة", "Access activation falsely claimed")
    check(by_id["T02"]["status"] == "الصرف غير مؤكد", "Invoice payment falsely claimed")
    check(by_id["T07"]["status"] == "أعيد فتحها", "Reopened ticket status lost")
    check(by_id["T05"]["owner"] == "يوسف" and "نور" in by_id["T05"]["dependency"],
          "Report owner or dependency changed without evidence")
    check(by_id["T08"]["owner"] == "عمر", "Subscription ownership changed")

    # Validate local paths and all source anchors; external links are not fetched.
    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
            if "://" in target or target.startswith("mailto:"):
                continue
            relative, _, anchor = target.partition("#")
            destination = (path.parent / relative).resolve() if relative else path
            check(destination.is_relative_to(ROOT), f"Link leaves repository: {path.name}: {target}")
            check(destination.exists(), f"Broken local link: {path.relative_to(ROOT)}: {target}")
            if anchor and destination.name == "raw-input.md" and destination.exists():
                check(anchor.upper() in source_ids, f"Unknown source anchor: {target}")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    check("https://github.com/SDAIAAcademy" in readme, "Academy link missing")
    check("L0-FGP" in readme, "Reference training program missing")
    metadata = read_json("docs/project-metadata.json")
    expected_metadata = {
        "project_name": "Badil — بديل", "course_name": "Generative AI for Workplace Productivity",
        "course_code": "L0-FGP", "instructor": "Fahad Alqahtani",
        "trainee": "ibrahim abdullah alburaidi", "trainee_ar": "إبراهيم البريدي",
        "professional_scenario": "Operations Coordinator — Employee Handover and Work Continuity",
        "submission_date": "2026-09-15", "submission_date_display": "15 September 2026",
        "release": "v0.1.2", "github_account": "ibrahim-alburaidi",
        "publication_status": "approved",
    }
    for key, value in expected_metadata.items():
        check(metadata.get(key) == value, f"Project metadata mismatch: {key}")
    table_keys = {
        "Project Name": "project_name", "Course Name": "course_name", "Course Code": "course_code",
        "Instructor": "instructor", "Trainee": "trainee", "Professional Scenario": "professional_scenario",
        "Submission Date": "submission_date_display",
    }
    for file in ("README.md", "docs/training-program.md"):
        document = (ROOT / file).read_text(encoding="utf-8")
        for label, key in table_keys.items():
            rows = [line for line in document.splitlines() if line.startswith(f"| **{label}** |")]
            check(len(rows) == 1, f"Missing/duplicate course table field: {file}/{label}")
            if rows:
                value = rows[0].strip("|").split("|")[1].strip().replace("**", "")
                check(value == metadata[key], f"Course table mismatch: {file}/{label}")
        check("[@SDAIAAcademy](https://github.com/SDAIAAcademy)" in document,
              f"Academy table link missing: {file}")
    demo = (ROOT / "docs/demo-guide.md").read_text(encoding="utf-8")
    durations = re.findall(r"— (\d+) ثانية", demo)
    check(len(durations) == 7 and sum(map(int, durations)) == 300, "Demo duration must be 300 seconds")
    prompts = (ROOT / "01-prompt-engineering/prompt-library.md").read_text(encoding="utf-8")
    check(len(re.findall(r"^## P\d{2} —", prompts, re.M)) == 7, "Expected seven reusable prompts")


if __name__ == "__main__":
    try:
        validate()
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        errors.append(f"Invalid project structure or data: {exc}")
    if errors:
        print(f"FAIL: {len(errors)} issue(s), {checks} checks evaluated")
        for issue in errors:
            print("- " + issue)
        sys.exit(1)
    print(f"PASS: {checks} checks; 16 sources; 8 tasks; 7 prompts")
    print("Human semantic review and trainee sign-off remain required.")
