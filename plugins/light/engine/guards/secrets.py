"""No secret is written to a file, and no command prints one.

Blocks a key in a known format, in a write or in a command's own text, and a command that prints a secrets file.
Warns on a value that only looks like a key.
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
    r"\b(?:cat|less|more|head|tail|bat|nl|strings|xxd|od|base64|grep|egrep|fgrep|rg|ag|awk|sed|cut|sort|uniq|tac|jq|yq)\b[^|;&\n]*?"
    r"(?P<file>(?:[\w./~-]*/)?(?:\.env(?:\.[\w-]+)*|credentials|id_(?:rsa|ed25519|ecdsa|dsa)|[\w.-]+\.pem|\.netrc"
    r"|secrets?\.(?:json|ya?ml|toml|env)))(?=$|[\s|;&>)])"
)
SAFE = re.compile(r"\.env\.(?:example|sample|template|dist)$")
ECHO = re.compile(
    r"\b(?:echo|printf)\b[^|;&\n]*(?:\$\{?\w*(?:KEY|TOKEN|SECRET|PASSWORD|PASSWD)\w*|\$\(\s*gh\s+auth\s+token|`\s*gh\s+auth\s+token)"
    r"|\bprintenv\s+\w*(?:KEY|TOKEN|SECRET|PASSWORD|PASSWD)\w*"
)
DUMP = re.compile(r"(?:^|[;&|]\s*)(?:printenv|env)\s*(?:$|[|;&>])", re.M)
# How a command is read: lines joined where they end in a backslash, comments dropped, then pipelines of simple
# commands split outside quotes, each heredoc body kept with the command that opened it. Rough on purpose: it reads
# what an agent writes by accident, not what someone writes to get past it. The older checks on the whole command
# (a secrets file read, a secret variable echoed) stay underneath it, so it can only add to what they block.
HEREDOC = re.compile(r"(?<!<)<<(?!<)-?\s*(?:(?P<quote>['\"])(?P<qword>[A-Za-z_]\w*)(?P=quote)|(?P<escaped>\\)?(?P<word>[A-Za-z_]\w*))")
ENV = re.compile(r"""^\s*(?:(?:\w+=(?:"[^"]*"|'[^']*'|\$\([^)]*\)|`[^`]*`|\S*)|\d?>>?\s*\S+)\s+)*""")
TO_FILE = re.compile(r"(?<!<)(?:&>>?|1?(?<![2<])>>?\|?)\s*(?!&)(?!/dev/(?:null|stdout|stderr|tty)\b)[^\s&|;)]|\btee\b|\bdd\b[^|;&\n]*\bof=")
TO_TERMINAL = re.compile(r">\s*/dev/(?:stdout|stderr|tty)\b")
IN_PLACE = re.compile(r"\b(?:sed|perl)\b[^|;&\n]*\s(?:-[a-zA-Z]*i[a-zA-Z]*\b|--in-place\b)|\byq\b[^|;&\n]*\s(?:-[a-zA-Z]*i\b|--inplace\b)")
PRINTER = re.compile(r"(?:echo|printf|cat)\b")
FILTER = re.compile(r"(?:tr|cut|rev|base64|xxd|od|head|tail|sort|uniq|sed|awk|jq|yq|cat|fold|column|grep)\b")
INTERPRETER = re.compile(r"(?:python[\d.]*|node|ruby|perl|php|bash|sh|zsh)\b")
INLINE = re.compile(r"\b(?:python[\d.]*|node|ruby|perl|php)\s+(?:-[a-zA-Z]*[cepr]\b|--eval\b|--print\b)|\bawk\s+['\"]")
SUBSTITUTION = re.compile(r"\bs(?P<d>[/|#,:@])(?P<pat>(?:\\.|(?!(?P=d)).)*)(?P=d)(?P<rep>(?:\\.|(?!(?P=d)).)*)(?P=d)")
DELETION = re.compile(r"/(?P<pat>(?:\\.|[^/])*)/\s*d\b")
GIT_STORE = re.compile(r"\bgit(?:\s+-[Cc]\s+\S+|\s+--?[\w-]+(?:=\S+)?)*\s+(?:clone|config|remote\s+(?:add|set-url)|submodule\s+add)\b")
APPLY_PATCH = re.compile(r"\bapply_patch\b")
LOGIN = re.compile(r"\|\s*[^|;&\n]*--(?:password-stdin|with-token)\b")
# A secret held in a variable, or fetched by a command, as the shell expands it. A name for a path is not one.
SECRET_VAR = (r"\$\{?(?!\w*_(?:PATH|FILE|DIR|NAME)\b)\w*(?:KEY|TOKEN|SECRET|PASSWORD|PASSWD)\w*\}?"
              r"|\$\(\s*gh\s+auth\s+token\s*\)|`\s*gh\s+auth\s+token\s*`")
GH_TOKEN = re.compile(r"gh\s+auth\s+(?:token\b|status\b[^|;&\n]*--show-token\b)")
# The header of a private key names the format and holds no secret, so it counts only where a command writes or runs code.
PRIVATE = "a private key"


def _blank(text, quotes="'"):
    """A command with the inside of its quoted strings emptied, read in order as the shell reads them.

    Single quotes expand nothing, so what they hold is never a variable. A `>` inside any quotes redirects nothing.
    An apostrophe inside double quotes opens nothing.
    """
    out, quote, i = [], None, 0
    while i < len(text):
        c = text[i]
        if quote:
            if c == "\\" and quote == '"' and i + 1 < len(text):
                if quote not in quotes:
                    out.append(text[i:i + 2])
                i += 2
                continue
            if c == quote:
                quote = None
                out.append(c)
            elif quote not in quotes:
                out.append(c)
        elif c == "\\" and i + 1 < len(text):
            out.append(text[i:i + 2])  # an escaped character outside quotes opens nothing
            i += 2
            continue
        else:
            if c in "'\"":
                quote = c
            out.append(c)
        i += 1
    return "".join(out)


def _heredocs(text):
    """The heredocs a command opens, leaving out a `<<` that sits inside a quoted string."""
    out = []
    for doc in HEREDOC.finditer(text):
        before = _blank(text[:doc.start()], "'\"")
        if before.count("'") % 2 == 0 and before.count('"') % 2 == 0 and not re.search(r"(?:^|\s)#", before):
            out.append(doc)
    return out


def _scan(skeleton):
    """Comments dropped and simple commands split, outside quotes: (command, the operator after it)."""
    parts, buf, quote, i, n = [], "", None, 0, len(skeleton)
    while i < n:
        c = skeleton[i]
        if quote:
            buf += c
            if c == "\\" and quote == '"' and i + 1 < n:
                buf, i = buf + skeleton[i + 1], i + 1
            elif c == quote:
                quote = None
        elif c == "\\" and i + 1 < n:
            buf, i = buf + skeleton[i:i + 2], i + 2
            continue
        elif c == "#" and (not buf or buf[-1] in " \t\n;&|("):
            while i < n and skeleton[i] != "\n":
                i += 1
            continue
        elif c in "'\"`":
            quote, buf = c, buf + c
        elif skeleton.startswith(("&&", "||"), i):
            parts.append((buf, skeleton[i:i + 2]))
            buf, i = "", i + 1
        elif c == "|" and buf.endswith(">"):
            buf += c  # `>|` is a redirect, not a pipe
        elif c in ";|\n" or (c == "&" and not buf.endswith(">") and not skeleton.startswith(">", i + 1)):
            parts.append((buf, c))
            buf = ""
        else:
            buf += c
        i += 1
    parts.append((buf, None))
    return [(text, op) for text, op in parts if text.strip()]


def pipelines(command):
    """The command as pipelines, each a list of (simple command, its heredoc bodies as (quoted, body))."""
    lines = re.sub(r"\\\r?\n", "", command or "").split("\n")  # the shell drops a backslash-newline whole
    skeleton, bodies, i = [], [], 0
    while i < len(lines):
        line = lines[i]
        skeleton.append(line)
        i += 1
        for doc in _heredocs(line):
            word, body = doc.group("qword") or doc.group("word"), []
            while i < len(lines) and lines[i].strip() != word:
                body.append(lines[i])
                i += 1
            i += 1
            bodies.append((bool(doc.group("quote") or doc.group("escaped")), "\n".join(body)))
    out, current = [], []
    for text, op in _scan("\n".join(skeleton)):
        docs = [bodies.pop(0) for _ in _heredocs(text) if bodies]
        current.append((text, docs))
        if op != "|":
            out.append(current)
            current = []
    if current:
        out.append(current)
    return out


def known(text):
    """The name of the first known key format in a text, or None."""
    for name, pattern in KNOWN:
        if pattern.search(text or ""):
            return name
    return None


def held(text, private=False):
    """The name and the matches of a known key that a command's text holds, judged as a command and not as a file."""
    for name, pattern in KNOWN:
        if name == PRIVATE and not private:
            continue
        found = [m.group(0) for m in pattern.finditer(text or "")]
        if name == "an OpenAI key":
            found = [f for f in found if re.search(r"\d", f) and re.search(r"[A-Z]", f)]  # a slug is not a key
        if found:
            return name, found
    return None, []


def _adds(text, keys):
    """Whether an in-place edit puts a key in: anywhere but where it is matched to be replaced or deleted."""
    if re.search(r"\byq\b", text):
        return True
    rest = DELETION.sub("", SUBSTITUTION.sub(lambda m: m.group("rep"), text))
    return any(k in rest for k in keys)


def _assigned(command):
    """The names a command assigns a known key to, so the key is followed through them."""
    names = set()
    for found in re.finditer(r"\b(\w+)=['\"]?(\S+)", command or ""):
        if held(found.group(2))[0]:
            names.add(found.group(1))
    return names


def command_findings(command, judge_keys=True):
    """What the command half of the guard says: (message, instead), the first that applies."""
    assigned = _assigned(command)
    secret = re.compile(SECRET_VAR + "".join(r"|\$\{?" + re.escape(a) + r"\b" for a in assigned))
    for pipe in pipelines(command):
        bares = [ENV.sub("", text) for text, _ in pipe]
        texts = [text + "\n" + "\n".join(body for _, body in docs) for text, docs in pipe]
        writes = any(TO_FILE.search(_blank(text, "'\"")) for text, _ in pipe)
        last, last_bare = pipe[-1][0], bares[-1]
        on_screen = not TO_FILE.search(_blank(last, "'\"")) and (
            bool(PRINTER.match(last_bare) or TO_TERMINAL.search(last))
            or (len(pipe) > 1 and bool(PRINTER.match(bares[0])) and bool(FILTER.match(last_bare))
                and not re.match(r"grep\b[^|;&\n]*\s-[a-zA-Z]*q", last_bare)))
        for (text, docs), bare, full in zip(pipe, bares, texts) if judge_keys else ():
            code = bool(INLINE.search(text) or (docs and INTERPRETER.match(bare)))
            name, keys = held(full, private=writes or code)
            if not name:
                continue
            if GIT_STORE.search(text):
                return (f"The command would store {name} in git's config, inside an address.",
                        "let git ask for it, or use a credential helper. Never put a key in an address.")
            if IN_PLACE.search(text):
                if _adds(text, keys):
                    return (f"The command would write {name} into a file in place.",
                            "write the variable's name, so the file reads the value at run time.")
                continue  # a key taken out of a file is the fix, not the leak
            if writes or on_screen or code:
                verb = "write" if writes else "run code that holds" if code else "print"
                return (f"The command would {verb} {name} that its own text holds.",
                        "read the value from the environment. If the person must store the key, they do it themselves.")
        for text, docs in pipe:
            if writes and any(not quoted and secret.search(body) for quoted, body in docs):
                return ("The command would expand a secret variable into a file, through an unquoted heredoc.",
                        "quote the heredoc's word, `<<'EOF'`, so the file holds the variable's name and reads it at run time.")
            if IN_PLACE.search(text) and secret.search(_blank(text)):
                return ("The command would expand a secret variable into a file in place.",
                        "write the variable's name, so the file reads the value at run time.")
            if writes and "<<<" in text and secret.search(_blank(text.split("<<<", 1)[1])):
                return ("The command would expand a secret variable into a file.",
                        "write the variable's name, so the file reads the value at run time.")
        for index, bare in enumerate(bares):
            if GH_TOKEN.match(bare) and (writes or (index == len(pipe) - 1 and not re.search(r">\s*/dev/null", pipe[index][0]))):
                return ("The command would " + ("write" if writes else "print") + " the GitHub CLI's token.",
                        "pass it where it is needed as `$(gh auth token)`, so it is never printed.")
        login = any(LOGIN.search(" | " + text) for text, _ in pipe[1:])
        for text, docs in pipe:
            run = [body for _, body in docs] if docs and not TO_FILE.search(_blank(text, "'\"")) else []
            if any(ECHO.search(_blank(body)) for body in run) and not login:
                return ("The command would print a secret variable, inside a heredoc it runs.",
                        "check that it is set without printing it, for example `test -n \"$NAME\"`.")
            if ECHO.search(_blank(text)) and (writes or not login):
                verb = "write" if writes else "print"
                return (f"The command would {verb} a secret variable.",
                        "check that it is set without printing it, for example `test -n \"$NAME\"`.")
        if assigned and (writes or on_screen) and any(
                re.search(r"\b(?:echo|printf)\b", text) and secret.search(_blank(text)) for text, _ in pipe):
            return ("The command would " + ("write" if writes else "print") + " a key it assigned to a variable.",
                    "read the value from the environment. If the person must store the key, they do it themselves.")
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
        # A patch is judged by its writes above, where the project's `skip` applies, even when it excused them all.
        patch = bool(call.writes) or bool(APPLY_PATCH.search(call.command) and "*** Begin Patch" in call.command)
        said = command_findings(call.command, judge_keys=not patch)
        if said:
            out.append(Finding(NAME, "block", said[0], RULE, said[1]))
        elif reads and not SAFE.search(reads.group("file")):
            out.append(Finding(NAME, "block", f"The command prints a secrets file, `{reads.group('file')}`.", RULE,
                               "check that the value is set without printing it, for example `test -n \"$NAME\"`."))
        elif DUMP.search(call.command):
            out.append(Finding(NAME, "warn", "The command prints every environment variable, secrets included.", RULE,
                               "name the one variable you need."))
    return out
