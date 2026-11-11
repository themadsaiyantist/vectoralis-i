"""The hook entry point, end to end: a real payload on stdin, the exit code and the answer on the way out.

Run with `python3 -m unittest discover -s tests -q`. Every test builds its own temporary project.
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "plugins" / "light" / "hooks" / "run.py"
DONE, OPEN = "✅", "⬜"
TOKEN = "ghp_" + "a" * 36


class Hooks(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory(prefix="vectoralis-test-")
        self.root = Path(self.folder.name).resolve()
        self.session = "test-" + uuid.uuid4().hex
        self.home = tempfile.TemporaryDirectory(prefix="vectoralis-home-")
        self.addCleanup(self.home.cleanup)
        self.addCleanup(self.folder.cleanup)

    def put(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def settings(self, approve=True, **more):
        base = {"profile": "light", "test": "", "format": ""}
        base.update(more)
        self.put("harness/settings.json", json.dumps(base))
        if approve:
            self.trust()

    def trust(self):
        env = dict(os.environ, VECTORALIS_HOME=self.home.name)
        env.pop("CLAUDE_PROJECT_DIR", None)
        subprocess.run([sys.executable, str(ROOT / "plugins" / "light" / "bin" / "vectoralis"), "trust"], cwd=str(self.root),
                       capture_output=True, env=env, check=True)

    def hook(self, event, env=None, **payload):
        payload.setdefault("session_id", self.session)
        payload.setdefault("cwd", str(self.root))
        clean = {k: v for k, v in os.environ.items() if k not in ("CLAUDE_PROJECT_DIR", "PLUGIN_ROOT")}
        clean.update(VECTORALIS_HOME=self.home.name, TMPDIR=self.home.name)
        clean.update(env or {})
        return subprocess.run([sys.executable, str(RUN), event], input=json.dumps(payload), capture_output=True,
                              text=True, env=clean, timeout=60)

    def test_claude_write_with_a_token_is_blocked(self):
        done = self.hook("write", tool_name="Write",
                         tool_input={"file_path": str(self.root / "config.py"), "content": f'token = "{TOKEN}"\n'})
        self.assertEqual(done.returncode, 2)
        self.assertIn("BLOCKED by Vectoralis. Nothing was written.", done.stderr)
        self.assertIn("Do instead:", done.stderr)

    def test_claude_edit_scans_only_the_new_text(self):
        path = self.put("config.py", f'old = "{TOKEN}"\nname = "x"\n')
        done = self.hook("write", tool_name="Edit",
                         tool_input={"file_path": str(path), "old_string": 'name = "x"', "new_string": 'name = "y"'})
        self.assertEqual(done.returncode, 0, done.stderr)

    def test_codex_patch_with_a_token_is_blocked(self):
        patch = f'*** Begin Patch\n*** Add File: config.py\n+token = "{TOKEN}"\n*** End Patch\n'
        done = self.hook("write", env={"PLUGIN_ROOT": str(ROOT / "plugins" / "light")},
                         tool_name="apply_patch", tool_input={"command": patch})
        self.assertEqual(done.returncode, 2)
        self.assertIn("config.py", done.stderr)

    def test_a_warning_reaches_the_agent_as_context_and_does_not_block(self):
        done = self.hook("write", tool_name="Write", tool_input={
            "file_path": str(self.root / "s.py"), "content": 'api_key = "9f8e7d6c5b4a39281706f5e4d3c2b1a0"\n'})
        self.assertEqual(done.returncode, 0)
        out = json.loads(done.stdout)["hookSpecificOutput"]
        self.assertEqual(out["hookEventName"], "PreToolUse")
        self.assertIn("looks like a secret", out["additionalContext"])

    def test_a_clean_write_passes_in_silence(self):
        done = self.hook("write", tool_name="Write", tool_input={"file_path": str(self.root / "a.py"), "content": "x = 1\n"})
        self.assertEqual((done.returncode, done.stdout, done.stderr), (0, "", ""))

    def test_stop_blocks_while_the_tests_fail_and_never_twice(self):
        self.settings(test="echo 'FAILED test_total' && exit 1")
        self.hook("wrote", tool_name="Write", tool_input={"file_path": str(self.put("a.py", "x = 1\n")), "content": "x = 1\n"})
        done = self.hook("stop")
        self.assertEqual(done.returncode, 2)
        self.assertIn("NOT DONE YET", done.stderr)
        self.assertIn("FAILED test_total", done.stderr)
        self.assertEqual(self.hook("stop", stop_hook_active=True).returncode, 0)

    def test_stop_tells_the_person_when_the_tests_pass(self):
        self.settings(test="true")
        self.hook("wrote", tool_name="Write", tool_input={"file_path": str(self.put("a.py", "x = 1\n")), "content": "x = 1\n"})
        done = self.hook("stop")
        self.assertEqual(done.returncode, 0)
        self.assertIn("they pass", json.loads(done.stdout)["systemMessage"])

    def test_stop_answers_codex_in_json_even_with_nothing_to_say(self):
        self.settings()
        done = self.hook("stop", env={"PLUGIN_ROOT": str(ROOT / "plugins" / "light")})
        self.assertEqual((done.returncode, json.loads(done.stdout)), (0, {}))

    def test_a_command_from_a_cloned_repository_does_not_run_until_it_is_approved_here(self):
        self.settings(approve=False, test="echo 'FAILED cloned' && exit 1")
        write = dict(tool_name="Write", tool_input={"file_path": str(self.put("a.py", "x = 1\n")), "content": "x = 1\n"})
        self.hook("wrote", **write)
        waiting = self.hook("stop")
        self.assertEqual(waiting.returncode, 0)
        self.assertIn("nobody approved it on this machine", json.loads(waiting.stdout)["systemMessage"])
        self.trust()
        self.hook("wrote", **write)
        self.assertEqual(self.hook("stop").returncode, 2)
        self.settings(approve=False, test="echo 'FAILED changed' && exit 2")
        self.hook("wrote", **write)
        self.assertEqual(self.hook("stop").returncode, 0)

    def test_stop_is_silent_when_nothing_changed(self):
        self.settings(test="exit 1")
        done = self.hook("stop")
        self.assertEqual((done.returncode, done.stdout), (0, ""))

    def test_a_projects_own_guard_runs_in_a_light_project_too(self):
        self.settings()
        self.put("harness/guards/debug-print.json", json.dumps({
            "id": "debug-print", "on": "write", "path": "src/**/*.py", "pattern": "^\\s*print\\(", "mode": "warn",
            "message": "A debug print is about to ship.", "instead": "use the logger.",
            "payloads": [{"name": "hit", "path": "src/a.py", "text": "print(x)", "expect": "hit"},
                         {"name": "pass", "path": "src/a.py", "text": "log(x)", "expect": "pass"}]}))
        call = lambda text: self.hook("write", tool_name="Write", tool_input={"file_path": str(self.root / "src/a.py"), "content": text})
        warned = call("print(total)\n")
        self.assertEqual(warned.returncode, 0)
        note = json.loads(warned.stdout)["hookSpecificOutput"]["additionalContext"]
        self.assertIn("A debug print is about to ship.", note)
        self.assertIn("use the logger.", note)
        self.assertEqual(call("log.info(total)\n").stdout, "")

    def test_a_heavy_guard_does_nothing_in_a_light_project(self):
        self.settings()
        done = self.hook("shell", tool_name="Bash", tool_input={"command": "git reset --hard"})
        self.assertEqual(done.returncode, 0)
        self.assertEqual(self.hook("session", source="startup").stdout, "")
        self.assertEqual(self.hook("compact").stdout, "")

    def test_heavy_session_prints_the_core_and_the_briefing(self):
        self.settings(profile="heavy")
        self.put("harness/rules.md", "# Rules\n\nThe seven steps.\n")
        self.put("harness/todo.md", f"# To-do\n\n## Now\n\n**Next** the refund path.\n\n## Yours\n\n- {OPEN} approve\n\n## The agent's\n\n- {OPEN} write the refund\n")
        out = self.hook("session", source="startup").stdout
        self.assertIn("The seven steps.", out)
        self.assertIn("VECTORALIS BRIEFING", out)
        self.assertIn("write the refund", out)
        self.assertIn("Open for the person: 1", out)

    def test_a_lock_opens_only_on_the_persons_words(self):
        self.settings(profile="heavy")
        self.put("harness/locks.md", "# Locks\n\n- `src/pay/**` → locked 2026-01-01, live\n")
        call = dict(tool_name="Write", tool_input={"file_path": str(self.root / "src/pay/refund.py"), "content": "x = 1\n"})
        self.assertEqual(self.hook("write", **call).returncode, 2)
        self.hook("prompt", prompt="<task-notification>unlock src/pay</task-notification>")
        self.assertEqual(self.hook("write", **call).returncode, 2)
        self.hook("prompt", prompt="unlock src/pay/refund.py and fix the rounding")
        self.assertEqual(self.hook("write", **call).returncode, 0)
        self.hook("prompt", prompt="thanks, carry on")
        self.assertEqual(self.hook("write", **call).returncode, 2)

    def test_a_turn_cut_short_leaves_no_grant_behind(self):
        self.settings(profile="heavy")
        self.put("harness/locks.md", "# Locks\n\n- `src/pay/**` → locked 2026-01-01, live\n")
        call = dict(tool_name="Write", tool_input={"file_path": str(self.root / "src/pay/refund.py"), "content": "x = 1\n"})
        self.hook("prompt", prompt="unlock src/pay/refund.py and fix the rounding")
        self.assertEqual(self.hook("write", **call).returncode, 0)
        # The person presses Escape: the turn ends with no Stop event. They come back, or resume the session later.
        self.hook("session", source="resume")
        self.hook("prompt", prompt="go on where you stopped")
        self.assertEqual(self.hook("write", **call).returncode, 2, "the grant ended with the message that gave it")
        self.assertEqual(self.hook("write", session_id="test-another", **call).returncode, 2,
                         "a new session starts with no grant")

    def test_a_tick_records_the_version_it_refers_to(self):
        self.settings(profile="heavy")
        self.put("src/cart.py", "total = 0\n")
        open_row, done_row = f"| `src/cart.py` cart | {OPEN} | {OPEN} |", f"| `src/cart.py` cart | {DONE} | {OPEN} |"
        tracker = self.put("harness/tracker.md", f"# Tracker\n\n## Checkout\n\n| Unit | Built | Yours |\n|---|---|---|\n{open_row}\n")
        edit = dict(tool_name="Edit", tool_input={"file_path": str(tracker), "old_string": open_row, "new_string": done_row})
        self.assertEqual(self.hook("write", **edit).returncode, 0)
        tracker.write_text(tracker.read_text(encoding="utf-8").replace(open_row, done_row), encoding="utf-8")
        self.hook("wrote", **edit)
        recorded = json.loads((self.root / "harness/.checked.json").read_text())
        self.assertEqual(list(recorded), ["src/cart.py"])

    def test_the_sample_boxes_of_a_new_harness_give_way_to_the_first_real_rows(self):
        env = dict(os.environ, VECTORALIS_HOME=self.home.name)
        env.pop("CLAUDE_PROJECT_DIR", None)
        subprocess.run([sys.executable, str(ROOT / "plugins" / "light" / "bin" / "vectoralis"), "init", "heavy"],
                       cwd=str(self.root), capture_output=True, env=env, check=True)
        tracker, todo = self.root / "harness" / "tracker.md", self.root / "harness" / "todo.md"
        sample = f"| the first unit of work | {OPEN} | {OPEN} | {OPEN} |"
        self.assertIn(sample, tracker.read_text(encoding="utf-8"))
        done = self.hook("write", tool_name="Edit", tool_input={
            "file_path": str(tracker), "old_string": sample,
            "new_string": f"| `src/cart.py` the cart total | {OPEN} | {OPEN} | {OPEN} |"})
        self.assertEqual(done.returncode, 0, done.stderr)
        mine = f"- {OPEN} the first thing only you can do"
        self.assertIn(mine, todo.read_text(encoding="utf-8"))
        done = self.hook("write", tool_name="Edit", tool_input={
            "file_path": str(todo), "old_string": mine, "new_string": f"- {OPEN} approve the copy"})
        self.assertEqual(done.returncode, 0, done.stderr)
        todo.write_text(todo.read_text(encoding="utf-8").replace(mine, f"- {OPEN} approve the copy"), encoding="utf-8")
        done = self.hook("write", tool_name="Edit", tool_input={
            "file_path": str(todo), "old_string": f"- {OPEN} approve the copy\n", "new_string": ""})
        self.assertEqual(done.returncode, 2)
        self.assertIn("An open box of the person's would be removed", done.stderr)

    def test_a_turn_that_fills_the_first_rows_of_a_new_harness_ends_clean(self):
        env = dict(os.environ, VECTORALIS_HOME=self.home.name)
        env.pop("CLAUDE_PROJECT_DIR", None)
        run = dict(cwd=str(self.root), capture_output=True, env=env, check=True)
        subprocess.run([sys.executable, str(ROOT / "plugins" / "light" / "bin" / "vectoralis"), "init", "heavy"], **run)
        subprocess.run(["git", "init", "-q"], **run)
        subprocess.run(["git", "add", "-A"], **run)
        subprocess.run(["git", "-c", "user.name=goku", "-c", "user.email=goku@example.com", "commit", "-q", "-m", "start"], **run)
        self.hook("prompt", prompt="fill the first rows of the tracker and the to-do list")
        tracker, todo = self.root / "harness" / "tracker.md", self.root / "harness" / "todo.md"
        text = tracker.read_text(encoding="utf-8").replace("First area", "Checkout")
        text = text.replace(f"| the first unit of work | {OPEN} | {OPEN} | {OPEN} |", f"| the cart total | {OPEN} | {OPEN} | {OPEN} |")
        tracker.write_text(text, encoding="utf-8")
        todo.write_text(todo.read_text(encoding="utf-8").replace("the first thing only you can do", "approve the copy"), encoding="utf-8")
        done = self.hook("stop")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.hook("prompt", prompt="tidy the to-do list")
        todo.write_text(todo.read_text(encoding="utf-8").replace(f"- {OPEN} approve the copy\n", ""), encoding="utf-8")
        done = self.hook("stop")
        self.assertEqual(done.returncode, 2)
        self.assertIn("An open box of the person's was removed this turn", done.stderr)

    def test_a_teammates_own_tick_that_arrives_with_their_commit_is_left_alone(self):
        self.settings(profile="heavy", team=True)
        head = "# Tracker\n\n## Checkout\n\n| Unit | Owner | Built | Yours |\n|---|---|---|---|\n"
        mine, hers = f"| the cart total | goku | {OPEN} | {OPEN} |", f"| refund | vegeta | {DONE} | {OPEN} |"
        between = "| one more | goku |  |  |\n| and one | goku |  |  |\n| and a third | goku |  |  |\n"
        tracker = self.put("harness/tracker.md", head + mine + "\n" + between + hers + "\n")
        self.put("harness/todo.md", f"# To-do\n\n## Yours, goku\n\n- {OPEN} approve the copy\n\n## The agent's\n\n- {OPEN} write the copy\n")
        run = dict(cwd=str(self.root), capture_output=True, check=True)
        for step in (["init", "-q"], ["config", "user.name", "goku"], ["config", "user.email", "goku@example.com"],
                     ["add", "-A"], ["commit", "-q", "-m", "start"]):
            subprocess.run(["git", *step], **run)

        def change(old, new):
            tracker.write_text(tracker.read_text(encoding="utf-8").replace(old, new), encoding="utf-8")

        def tick_hers(*how):
            change(hers, hers.replace(f"| {OPEN} |", f"| {DONE} |"))
            subprocess.run(["git", *how, "commit", "-q", "-am", "tick the refund"], **run)

        def back():
            subprocess.run(["git", "reset", "-q", "--hard", "HEAD~1"], **run)

        as_her = ("-c", "user.name=vegeta", "-c", "user.email=vegeta@example.com")
        self.hook("prompt", prompt="pull what the others pushed")
        tick_hers(*as_her)
        self.assertEqual(self.hook("stop").returncode, 0, "her own commit brought her own tick")
        back()
        self.hook("prompt", prompt="tick refund")
        tick_hers()
        done = self.hook("stop")
        self.assertEqual(done.returncode, 2)
        self.assertIn("it is vegeta's", done.stderr)
        back()
        self.hook("prompt", prompt="tick refund")
        change(hers, hers.replace(f"| {OPEN} |", f"| {DONE} |"))
        subprocess.run(["git", "commit", "-q", "-am", "tick the refund", "--author=vegeta <vegeta@example.com>"], **run)
        self.assertEqual(self.hook("stop").returncode, 2, "an author's name is a claim, the committer is the machine")
        back()
        subprocess.run(["git", "checkout", "-q", "-b", "theirs"], **run)
        tick_hers(*as_her)
        subprocess.run(["git", "checkout", "-q", "-"], **run)
        self.hook("prompt", prompt="build the cart total, then pull")
        change(mine, mine.replace(f"| goku | {OPEN} |", f"| goku | {DONE} |"))
        subprocess.run(["git", "commit", "-q", "-am", "the cart total is built"], **run)
        subprocess.run(["git", "merge", "-q", "--no-edit", "theirs"], **run)
        done = self.hook("stop")
        self.assertEqual(done.returncode, 0, done.stderr)
        back()
        subprocess.run(["git", "checkout", "-q", "theirs"], **run)
        change(hers.replace(f"| {OPEN} |", f"| {DONE} |"), hers)
        subprocess.run(["git", *as_her, "commit", "-q", "-am", "she takes it back"], **run)
        subprocess.run(["git", "checkout", "-q", "-"], **run)
        self.hook("prompt", prompt="tick refund")
        subprocess.run(["git", "merge", "-q", "--no-edit", "theirs"], **run)
        change(hers, hers.replace(f"| {OPEN} |", f"| {DONE} |"))
        self.assertEqual(self.hook("stop").returncode, 2, "a tick she took back is not hers any more")
        back()
        subprocess.run(["git", "checkout", "-q", "-b", "again"], **run)
        tick_hers(*as_her)
        subprocess.run(["git", "checkout", "-q", "-"], **run)
        self.hook("prompt", prompt="pull, then rename the section")
        subprocess.run(["git", "merge", "-q", "--no-edit", "again"], **run)
        change("## Checkout", "## Cart")
        done = self.hook("stop")
        self.assertEqual(done.returncode, 0, "her tick is known by where it stood before the rename: " + done.stderr)

    def test_an_edit_by_hand_between_two_turns_is_not_the_agents(self):
        self.settings(profile="heavy")
        cart, refund = f"| the cart total | {DONE} | {DONE} | {OPEN} |", f"| refund | {DONE} | {OPEN} | {OPEN} |"
        checked = f"| refund | {DONE} | {DONE} | {OPEN} |"
        head = "# Tracker\n\n## Checkout\n\n| Unit | Built | Checked | Yours |\n|---|---|---|---|\n"
        tracker = self.put("harness/tracker.md", f"{head}{cart}\n{refund}\n")
        run = dict(cwd=str(self.root), capture_output=True, check=True)
        for step in (["init", "-q"], ["add", "-A"], ["-c", "user.name=goku", "-c", "user.email=goku@example.com", "commit", "-q", "-m", "start"]):
            subprocess.run(["git", *step], **run)

        def change(old, new):
            tracker.write_text(tracker.read_text(encoding="utf-8").replace(old, new), encoding="utf-8")

        self.hook("prompt", prompt="read the cart total")
        self.assertEqual(self.hook("stop").returncode, 0)
        change(cart, cart[:-3] + f"{DONE} |")  # the person, in their editor, between two turns
        self.hook("prompt", prompt="check the refund")
        work = dict(tool_name="Write", tool_input={"file_path": str(self.put("src/refund.py", "x = 1\n")), "content": "x = 1\n"})
        self.hook("wrote", **work)
        change(refund, checked)
        done = self.hook("stop")
        self.assertEqual(done.returncode, 0, "a box the person ticked before the turn began is theirs: " + done.stderr)
        self.hook("prompt", prompt="finish the refund")
        self.hook("wrote", **work)
        change(checked, checked[:-3] + f"{DONE} |")  # the person's box, ticked inside a turn
        done = self.hook("stop")
        self.assertEqual(done.returncode, 2, "inside a turn, the person's box is not the agent's to tick")
        self.assertIn("refund", done.stderr)

    def test_a_subagent_cannot_write_a_record(self):
        self.settings(profile="heavy")
        done = self.hook("write", agent_id="agent-7", tool_name="Write",
                         tool_input={"file_path": str(self.root / "harness/tracker.md"), "content": "# Tracker\n"})
        self.assertEqual(done.returncode, 2)
        self.assertIn("subagent", done.stderr)

    def test_the_compaction_prompt_names_what_to_keep(self):
        self.settings(profile="heavy")
        self.hook("prompt", prompt="start on the cart")
        self.hook("wrote", tool_name="Write", tool_input={"file_path": str(self.put("src/a.py", "x\n")), "content": "x\n"})
        self.hook("prompt", prompt="unlock docs")
        self.hook("wrote", tool_name="Write", tool_input={"file_path": str(self.put("src/b.py", "x\n")), "content": "x\n"})
        out = self.hook("compact").stdout
        self.assertIn("src/a.py, src/b.py", out)
        self.assertIn("Keep these in the summary", out)
        self.assertIn("src/a.py", out)
        self.assertIn("unlock docs", out)

    def test_a_broken_payload_steps_aside_and_never_blocks(self):
        env = dict(os.environ, TMPDIR=self.home.name, VECTORALIS_HOME=self.home.name)
        done = subprocess.run([sys.executable, str(RUN), "write"], input="not json", capture_output=True, text=True, timeout=60, env=env)
        self.assertEqual(done.returncode, 0)


if __name__ == "__main__":
    unittest.main()
