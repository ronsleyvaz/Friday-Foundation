<!-- Built by Friday​‌‍‌​ (https://friday.amplifyais.com). Free for personal use. Commercial use needs a paid Friday. Licence: PolyForm-Noncommercial-1.0.0. -->

# Releasing Friday Shortcuts

`main` is the integration branch. Every merge lands here after CI passes.
`release` is the distribution branch: the installer and the README's install
one-liner both pull from it. Nothing reaches a fresh install until `release`
is deliberately advanced.

## Cutting a release

Fast-forward `release` to the current `main`:

```
git push origin main:release
```

That is the whole promote step. It is a fast-forward push, so it only
succeeds if `release` has no commits `main` does not already have, which is
always true since `release` only ever advances by this command.

## Before you run it, if the batch adds a command

The usage receiver on friday.amplifyais.com accepts only the command names
and output folder forms it already knows. When a merged pull request adds a
command name or a new folder form, deploy that allowlist (and the Monday
recap pairing) on the site and check it on the real domain first, then bump
`VERSION`, then promote. Promote first and every run of the new command from
a fresh install is a 400 the founder never sees, and `/friday-upgrade` tells
existing installs there is nothing to upgrade.

## When to run it

Run it after a batch of merged pull requests has been reviewed on `main` and
you are ready for new installs to pick them up. There is no fixed cadence; a
release is a deliberate act, not a side effect of merging.

## Rolling back a bad release

If a promoted change turns out to be broken, point `release` back at the
last good commit:

```
git push origin <previous-good-sha>:release --force-with-lease
```

This is a force push and rewrites `release` history. It needs explicit
maintainer intent, not something to run reflexively. Confirm the previous
good SHA first (`git log release`), and only run this after a genuinely
broken release has already shipped to installers.

---

Built by Amplify AI at amplifyais.com
