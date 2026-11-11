"""No secret is written to a file, and no command prints one.

Blocks a key in a known format and a command that prints a secrets file. Warns on a value that only looks like a key.
"""
from __future__ import annotations

import re

from . import Finding

NAME = "secrets"
RULE = "no secret is written to a file or printed (guard `secrets`)"
KNOWN = [
    ("an AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("a GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,}\b")),
    ("a GitHub token", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{40,}\b")),
    ("an Anthropic key", re.compile(r"\bsk-ant-[A-Za-z0-9_-]{20,}")),
    ("an OpenAI key", re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{32,}")),
    ("a Slack token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}")),
    ("a Stripe live key", re.compile(r"\b[sr]k_live_[A-Za-z0-9]{20,}")),
    ("a Google API key", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b")),
    ("a private key", re.compile(r"-----BEGIN (?:[A-Z]+ )?PRIVATE KEY-----")),
]
LOOKS = re.compile(r"(?i)\b(api[_-]?key|secret|token|passwd|password)\b[\"']?\s*[:=]\s*[\"']([^\"'\s]{20,})[\"']")
PLACEHOLDER = re.compile(r"(?i)example|your[_-]|xxxx|changeme|placeholder|dummy|<|\$\{|\{\{")
READS = re.compile(
    r"\b(?:cat|less|more|head|tail|bat|nl|strings|xxd|od|base64)\b[^|;&\n]*?"
    r"(?P<file>(?:[\w./~-]*/)?(?:\.env(?:\.[\w-]+)*|credentials|id_(?:rsa|ed25519|ecdsa|dsa)|[\w.-]+\.pem|\.netrc"
    r"|secrets?\.(?:json|ya?ml|toml|env)))(?=$|[\s|;&>)])"
)
SAFE = re.compile(r"\.env\.(?:example|sample|template|dist)$")
ECHO = re.compile(r"\b(?:echo|printf)\b[^|;&\n]*\$\{?\w*(?:KEY|TOKEN|SECRET|PASSWORD|PASSWD)\w*")
DUMP = re.compile(r"(?:^|[;&|]\s*)(?:printenv|env)\s*(?:$|[|;&>])", re.M)


def known(text):
    """The name of the first known key format in a text, or None."""
    for name, pattern in KNOWN:
        if pattern.search(text or ""):
            return name
    return None


def check(call, proj, state):
    out = []
    for write in call.writes:
        rel = proj.rel(write.path) or write.path
        if proj.skipped(NAME, rel):
            continue
        name = known(write.added)
        if name:
            out.append(Finding(NAME, "block", f"`{rel}` would hold {name}.", RULE,
                               "read the value from the environment, and keep it out of the repository."))
            continue
        looks = LOOKS.search(write.added or "")
        if looks and not PLACEHOLDER.search(looks.group(2)):
            out.append(Finding(NAME, "warn", f"`{rel}` gets a value that looks like a secret (`{looks.group(1)}`).", RULE,
                               "if it is real, read it from the environment."))
    if call.command:
        reads = READS.search(call.command)
        if reads and not SAFE.search(reads.group("file")):
            out.append(Finding(NAME, "block", f"The command prints a secrets file, `{reads.group('file')}`.", RULE,
                               "check that the value is set without printing it, for example `test -n \"$NAME\"`."))
        elif ECHO.search(call.command):
            out.append(Finding(NAME, "block", "The command prints a secret variable.", RULE,
                               "check that it is set without printing it, for example `test -n \"$NAME\"`."))
        elif DUMP.search(call.command):
            out.append(Finding(NAME, "warn", "The command prints every environment variable, secrets included.", RULE,
                               "name the one variable you need."))
    return out
