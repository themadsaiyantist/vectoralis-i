# Contributing

Issues are open and pull requests are welcome. Ten lines, and that is all of it.

1. **Open an issue first** for anything larger than a fix, so nobody builds what will not be merged.
2. **A pull request comes with the run that proves it:** the command you ran and what it printed.
3. **A change to a guard comes with a payload** that must act and one that must pass.
4. **A page keeps its shape:** what it is, a Contents line, then the sections `spec.md` gives it.
5. **Every claim carries its mark:** `run`, `read` or `referenced`, with the date.
6. **Plain words.** Bullets and arrows, no em or en dash, one line per paragraph.
7. **One fact, one home.** Link to it, never repeat it.
8. **Free and open first.** A paid tool is marked paid, with its price.
9. **Before you push:** `python3 -m unittest discover -s tests -q`, `python3 plugins/light/bin/vectoralis guards` and `python3 tools/check_writing.py`.
10. **Be kind in review.** Say what is wrong, how you know, and what would fix it.
