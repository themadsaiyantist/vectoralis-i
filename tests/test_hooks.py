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
        self.addCleanup(self.folder.cleanup)
        self.addCleanup(lambda: (Path(tempfile.gettempdir()) / "vectoralis" / (self.session + ".json")).unlink(missing_ok=True))

    def put(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def settings(self, **more):
        base = {"profile": "light", "test": "", "format": ""}
        base.update(more)
        self.put("harness/settings.json", json.dumps(base))

    def hook(self, event, env=None, **payload):
        payload.setdefault("session_id", self.session)
        payload.setdefault("cwd", str(self.root))
        clean = {k: v for k, v in os.environ.items() if k not in ("CLAUDE_PROJECT_DIR", "PLUGIN_ROOT")}
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

    def test_stop_is_silent_when_nothing_changed(self):
        self.settings(test="exit 1")
        done = self.hook("stop")
        self.assertEqual((done.returncode, done.stdout), (0, ""))

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
        done = subprocess.run([sys.executable, str(RUN), "write"], input="not json", capture_output=True, text=True, timeout=60)
        self.assertEqual(done.returncode, 0)


if __name__ == "__main__":
    unittest.main()
