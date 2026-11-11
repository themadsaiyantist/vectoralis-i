"""The `vectoralis` command: set a project up, show where it stands, prove the guards, check the records.

Run `vectoralis` with no argument for the list. It writes inside `harness/`, one line in `.gitignore`, and the commands
you approved in `~/.vectoralis/trusted.json`. With `--starter` it also writes an instructions file, only where none exists.
"""
from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
from pathlib import Path

from . import VERSION, briefing, checks, dashboard, prove, records, rules, trust
from .project import DEFAULT_MODES, HEAVY, LIGHT, Project, git

TEMPLATES = Path(__file__).resolve().parents[1] / "templates"
RECORDS = ("rules.md", "tracker.md", "todo.md", "failures.md", "lessons.md", "decisions.md", "locks.md")
INSTRUCTIONS = ("AGENTS.md", "AGENTS.override.md", "CLAUDE.md", "CLAUDE.local.md", ".claude/CLAUDE.md")


def detect_test(root) -> str:
    """The project's test command, read from the files it already has. Empty when none is found."""
    def has(name):
        return (root / name).is_file()

    def text(name):
        try:
            return (root / name).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            return ""

    if has("pytest.ini") or "[tool.pytest" in text("pyproject.toml") or "pytest" in text("requirements.txt"):
        return "python3 -m pytest -q"
    if any((root / "tests").glob("test_*.py")) or any(root.glob("test_*.py")):
        return "python3 -m unittest discover -s tests -q" if (root / "tests").is_dir() else "python3 -m unittest -q"
    if has("package.json"):
        try:
            script = (json.loads(text("package.json")).get("scripts") or {}).get("test", "")
        except ValueError:
            script = ""
        if script and "no test specified" not in script:
            return "npm test --silent"
    if has("Cargo.toml"):
        return "cargo test --quiet"
    if has("go.mod"):
        return "go test ./..."
    if re.search(r"(?m)^test:", text("Makefile")):
        return "make test"
    return ""


def detect_format(root) -> str:
    """The project's formatter, read from the files it already has. Empty when none is found."""
    def text(name):
        try:
            return (root / name).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            return ""

    pyproject, package = text("pyproject.toml"), text("package.json")
    if "[tool.ruff" in pyproject or (root / "ruff.toml").is_file():
        return "ruff format {file}"
    if "[tool.black" in pyproject:
        return "black -q {file}"
    if "prettier" in package or any(root.glob(".prettierrc*")):
        return "npx prettier --write {file}"
    if (root / "go.mod").is_file():
        return "gofmt -w {file}"
    if (root / "Cargo.toml").is_file():
        return "rustfmt {file}"
    return ""


def _ignore_dashboard(proj) -> bool:
    """Keep the dashboard out of git. True when the line had to be added."""
    ignore = proj.root / ".gitignore"
    lines = ignore.read_text(encoding="utf-8").splitlines() if ignore.is_file() else []
    if "harness/dashboard.html" in lines:
        return False
    ignore.write_text("\n".join(lines + ["harness/dashboard.html"]) + "\n", encoding="utf-8")
    return True


def cmd_init(args) -> int:
    proj = Project()
    proj.harness.mkdir(exist_ok=True)
    path = proj.harness / "settings.json"
    made, kept = [], []
    existed = path.is_file() and not proj.broken
    if existed:
        settings = dict(proj.settings)
    else:
        settings = {
            "profile": "light", "test": detect_test(proj.root), "test_timeout": 120,
            "format": detect_format(proj.root), "guards": {}, "skip": {}, "merge": "yours", "team": False,
        }
        made.append("harness/settings.json")
    if args.profile == "heavy":
        settings["profile"] = "heavy"
    if args.team:
        settings["team"] = True
    if existed:
        moved = [f"{key} is now {settings[key]}" for key in ("profile", "team") if settings.get(key) != proj.settings.get(key)]
        (made if moved else kept).append("harness/settings.json" + (" (" + ", ".join(moved) + ")" if moved else ""))
    had_records = (proj.harness / "tracker.md").exists() or (proj.harness / "todo.md").exists()
    path.write_text(json.dumps(settings, indent=2) + "\n", encoding="utf-8")
    proj.settings = settings
    if not existed:
        trust.approve(proj)  # init found these commands itself, in the project's own files
    if settings["profile"] == "heavy":
        person = git(proj.root, "config", "user.name").strip() or "you"
        for name in RECORDS:
            target = proj.harness / name
            if target.exists():
                kept.append(f"harness/{name}")
                continue
            team = TEMPLATES / name.replace(".md", ".team.md")
            source = team if settings.get("team") and team.is_file() else TEMPLATES / name
            target.write_text(source.read_text(encoding="utf-8").replace("{person}", person), encoding="utf-8")
            made.append(f"harness/{name}")
        if _ignore_dashboard(proj):
            made.append(".gitignore, one line")
    starter = not any((proj.root / name).exists() for name in INSTRUCTIONS)
    if args.starter and starter:
        commands = [f"- Run the tests \u2192 `{settings['test']}`"] if settings.get("test") else []
        commands += [f"- Format a file \u2192 `{settings['format']}`"] if settings.get("format") else []
        commands = commands or ["- Add the commands you run most here: the tests, the formatter."]
        body = (TEMPLATES / "AGENTS.md").read_text(encoding="utf-8")
        body = body.replace("{project}", proj.root.name).replace("{commands}", "\n".join(commands))
        (proj.root / "AGENTS.md").write_text(body, encoding="utf-8")
        (proj.root / "CLAUDE.md").write_text("@AGENTS.md\n", encoding="utf-8")
        made += ["AGENTS.md", "CLAUDE.md"]
        starter = False
    print(f"Vectoralis, the {settings['profile']} profile, in {proj.root}")
    print("Written: " + (", ".join(made) if made else "nothing"))
    if kept:
        print("Kept as they were: " + ", ".join(kept))
    if args.team and had_records:
        print("The tracker and the to-do list were kept. For a team, add an `Owner` column to the tracker "
              "and one `## Yours, name` section per person to the to-do list.")
    print("Tests: " + (f"`{settings['test']}`" if settings.get("test") else "no test command found. The `tests` guard is off until `test` is set in harness/settings.json."))
    print("Formatter: " + (f"`{settings['format']}`" if settings.get("format") else "none found. The `format` guard is off until `format` is set."))
    waiting = [kind for kind in trust.KINDS if not trust.trusted(proj, kind)]
    if waiting:
        print("Not approved on this machine yet: " + ", ".join(waiting) + ". A hook runs these commands, so read them, "
              "then run `vectoralis trust`.")
    if starter:
        print("No instructions file here. A starter is ready: `vectoralis init " + settings["profile"] + " --starter` writes AGENTS.md and a one-line CLAUDE.md.")
    else:
        print("Your instructions file is yours. Vectoralis does not edit it.")
    return 0


def cmd_status(args) -> int:
    proj = Project()
    if proj.profile != "heavy":
        print(f"Vectoralis, the light profile, in {proj.root}")
        for guard in LIGHT:
            print(f"  {guard}: {proj.mode(guard)}")
        return 0
    print(briefing.status_text(proj))
    return 0


def _guard_results():
    results = prove.run_all()
    failed = [r for r in results if not r["ok"]]
    return results, failed, prove.unproven(results)


def cmd_guards(args) -> int:
    proj = Project()
    results, failed, unproven = _guard_results()
    good_rules, bad_rules = rules.load(proj)
    wide = max([13] + [len(str(rule["id"])) + 2 for rule in good_rules])
    print(f"{'guard':<{wide}}{'here':<8}{'default':<9}proof")
    for guard in LIGHT + HEAVY:
        cases = [r for r in results if r["guard"] == guard]
        good = sum(1 for r in cases if r["ok"])
        proof = f"{good} of {len(cases)} payloads behave" if cases else "no payloads"
        print(f"{guard:<{wide}}{proj.mode(guard):<8}{DEFAULT_MODES[guard]:<9}{proof}")
    for rule in good_rules:
        print(f"{rule['id']:<{wide}}{rule.get('mode', 'warn'):<8}{'project':<9}its payloads behave")
    for line in bad_rules:
        print("NOT RUNNING: " + line)
    for result in failed:
        print(f"FAILED: {result['guard']}, \"{result['name']}\": expected {result['expect']}, got {result['got']}")
    for guard in unproven:
        print(f"UNPROVEN: {guard} needs one payload that acts and one that passes")
    slow = max((r["seconds"] for r in results if r["event"] != "stop"), default=0)
    print(f"{len(results)} payloads, the slowest answer took {slow * 1000:.0f} ms")
    return 1 if failed or unproven or bad_rules else 0


def cmd_budget(args) -> int:
    proj = Project()
    spent = checks.budget(proj)
    for name, chars, tokens in spent["rows"]:
        print(f"{tokens:>6}  {name}  ({chars} characters)")
    print(f"{spent['total']:>6}  always loaded, the cap for {proj.profile} is {spent['cap']}")
    print(f"Tokens are an estimate: characters divided by {checks.CHARS_PER_TOKEN}, the rate measured in live Claude Code sessions.")
    return 1 if spent["total"] > spent["cap"] else 0


def cmd_check(args) -> int:
    proj = Project()
    if proj.profile == "heavy":
        checks.sync(proj)
    flags = checks.stale(proj) if proj.profile == "heavy" else []
    _, failed, unproven = _guard_results()
    flags += [f"guard `{r['guard']}`: payload \"{r['name']}\" expected {r['expect']}, got {r['got']}" for r in failed]
    flags += [f"guard `{g}` has no proof" for g in unproven]
    if proj.profile != "heavy":
        spent = checks.budget(proj)
        if spent["total"] > spent["cap"]:
            flags.append(f"budget: about {spent['total']} tokens are always loaded, the cap is {spent['cap']}")
    for flag in flags:
        print("STALE: " + flag)
    print("Clean: every record is backed, every guard is proven, the core is under its cap." if not flags else f"{len(flags)} flag(s).")
    return 1 if flags else 0


def cmd_affirm(args) -> int:
    proj = Project()
    done = checks.affirm(proj, args.paths)
    for path in done:
        print(f"Recorded: `{path}` was checked again as it is now.")
    missing = [p for p in args.paths if (proj.rel(p) or p).rstrip("/") not in done]
    for path in missing:
        print(f"Not recorded: `{path}` is not bound to a ticked row of harness/tracker.md.")
    return 1 if missing else 0


def cmd_trust(args) -> int:
    proj = Project()
    found = trust.approve(proj)
    if not found:
        print("Nothing to approve: this project sets no test command and no formatter.")
        return 0
    print(f"Approved on this machine, for {proj.root}:")
    for kind, line in found:
        print(f"  {kind}: `{line}`")
    print("A hook runs these from now on. A change to either one needs a new approval.")
    return 0


def cmd_dashboard(args) -> int:
    proj = Project()
    if not proj.ready:
        print("No harness here. Run `vectoralis init heavy` first.")
        return 1
    _ignore_dashboard(proj)
    target = proj.harness / "dashboard.html"
    target.write_text(dashboard.build(proj), encoding="utf-8")
    print(target)
    return 0


def cmd_fail(args) -> int:
    proj = Project()
    path = proj.harness / "failures.md"
    if not path.is_file():
        print("No harness/failures.md here. Run `vectoralis init heavy` first.")
        return 1
    text = path.read_text(encoding="utf-8")
    slug = re.sub(r"[^a-z0-9]+", "-", args.klass.lower()).strip("-") or "unsorted"
    before = [f for f in records.failures(text) if f["class"] == slug]
    today = datetime.date.today().isoformat()
    entry = (
        f"### {records.OPEN} {today} · {args.who} · {args.title}\n\n**Class.** `{slug}`\n\n"
        f"**What failed.**\n\n**Cause.**\n\n**Fix.** {records.OPEN} the instance · {records.OPEN} the cause · {records.OPEN} the guard\n"
    )
    marker = "Newest first.\n"
    if marker in text:
        text = text.replace(marker, marker + "\n" + entry, 1)
    else:
        text = text.rstrip("\n") + "\n\n" + entry
    path.write_text(text, encoding="utf-8")
    print(f"Logged in harness/failures.md: {args.title}")
    if before:
        print(f"This class has failed before ({len(before)} time(s), first on {before[-1]['date']}).")
        print(f"Draft a guard: harness/guards/{slug}.json, in warn mode, with one payload that hits and one that passes.")
    return 0


def main(argv) -> int:
    parser = argparse.ArgumentParser(prog="vectoralis", description="A light and a heavy harness for coding agents.")
    sub = parser.add_subparsers(dest="command")
    init = sub.add_parser("init", help="set a project up: light or heavy")
    init.add_argument("profile", choices=("light", "heavy"))
    init.add_argument("--team", action="store_true", help="an owner on every row, a to-do section per person")
    init.add_argument("--starter", action="store_true", help="write a starter AGENTS.md where no instructions file exists")
    init.set_defaults(run=cmd_init)
    for name, run, text in (
        ("status", cmd_status, "where things stand, as a session start prints it"),
        ("check", cmd_check, "staleness, budget and every guard's proof. Exit 1 on any flag"),
        ("guards", cmd_guards, "every guard, its mode, and whether its payloads behave"),
        ("budget", cmd_budget, "what is always loaded, against the cap"),
        ("dashboard", cmd_dashboard, "write one HTML page and print its path"),
        ("trust", cmd_trust, "approve this project's test and format commands on this machine"),
    ):
        sub.add_parser(name, help=text).set_defaults(run=run)
    fail = sub.add_parser("fail", help="add an entry to the failure log")
    fail.add_argument("title")
    fail.add_argument("--class", dest="klass", required=True, help="a short slug. The second failure of a class asks for a guard")
    fail.add_argument("--who", default="agent")
    fail.set_defaults(run=cmd_fail)
    again = sub.add_parser("affirm", help="say a ticked file was checked again as it is now")
    again.add_argument("paths", nargs="+")
    again.set_defaults(run=cmd_affirm)
    sub.add_parser("version", help="the version").set_defaults(run=lambda a: print(VERSION) or 0)
    args = parser.parse_args(argv)
    if not getattr(args, "run", None):
        parser.print_help()
        return 0
    return args.run(args)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
