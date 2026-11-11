# Question round c

One call that is the author's, found while moving the CI actions to v7. Answer under the `Answer:` line, then say done.

**Contents:** The runner image

---

## The runner image

Every CI run now prints one notice: `ubuntu-latest` migrates to Ubuntu 26 beginning October 19, 2026 (https://github.com/actions/runner-images/issues/14748). The runs above still show Ubuntu 24.04.5, and all three Pythons pass on it. It was outside the scope given, so nothing was changed.

- **A (pick)** → leave `ubuntu-latest`. The workflow follows the new image, and a red run tells us if it breaks. Pull request 1 would not have needed a second change.
- **B** → pin `ubuntu-24.04` in `ci.yml`. The notice goes away and runs stay the same until a pin is moved by hand. The cost is a pin that goes stale and must be raised later.

Answer:
