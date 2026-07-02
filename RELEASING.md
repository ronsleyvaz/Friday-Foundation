# Releasing Friday Foundation

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
