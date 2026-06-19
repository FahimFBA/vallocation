# Changelog-driven release automation

## Goal

Maintain a hand-written `CHANGELOG.md` and automatically create a tagged GitHub Release whenever a new version section lands on `main`.

## CHANGELOG.md

- Location: repo root.
- Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), [Semantic Versioning](https://semver.org/).
- Structure:
  ```markdown
  # Changelog

  All notable changes to this project will be documented in this file.

  The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
  and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

  ## [Unreleased]

  ## [1.1.0] - 2026-06-19
  ### Security
  - ...
  ```
- Contributors add entries under `[Unreleased]` as they work. To cut a release, a maintainer renames `[Unreleased]` to `[X.Y.Z] - YYYY-MM-DD`, adds a fresh empty `[Unreleased]` above it, and pushes/merges to `main`.
- First entry: `[1.1.0] - 2026-06-19`, documenting today's dependency vulnerability fixes (Python deps bump, Docusaurus bump, npm `overrides` + `patch-package` patch for `gray-matter`).
- Covers the whole repo (API + docs site) as one unit — single version line, not split per component.

## Release workflow (`.github/workflows/release.yml`)

`taiki-e/parse-changelog` is a CLI tool, not a GitHub Action — it can't be used in a `uses:` step.

A two-workflow split (tag on `CHANGELOG.md` push → release on tag push) was tried and doesn't work: tags pushed using the default `GITHUB_TOKEN` don't trigger other workflows (GitHub's anti-recursion protection), so the second workflow never fires. Using a personal access token to work around that adds a secret to manage for no real benefit here, so instead everything happens in one workflow, one job — no tag-push trigger needed at all, because `create-gh-release-action` accepts an explicit `ref` input and creates the tag itself via the GitHub Releases API if it doesn't already exist.

- Trigger: `push` to `main`, `paths: ['CHANGELOG.md']`.
- Permissions: `contents: write` (to create the release/tag).
- Steps:
  1. `actions/checkout@v4` with `fetch-depth: 0` (full history, so existing tags are visible).
  2. Extract the first version header from `CHANGELOG.md` (first line matching `## [X.Y.Z] - `), via `grep -m1 -oP '(?<=^## \[)[0-9]+\.[0-9]+\.[0-9]+(?=\] - )' CHANGELOG.md`.
  3. If empty (top section is still `[Unreleased]`), set `skip=true` and stop — nothing to release.
  4. Check whether tag `v$VERSION` already exists (`git tag -l`). If it does, set `skip=true` and stop — this version was already released (e.g. an unrelated typo fix elsewhere in the file shouldn't trigger a re-release).
  5. Otherwise, run `taiki-e/create-gh-release-action@v1` with `changelog: CHANGELOG.md` and `ref: refs/tags/v$VERSION` — it parses that version's section out of `CHANGELOG.md` (via `parse-changelog` internally) and creates the tag + GitHub Release with that text as the body.

## Out of scope

- No automatic CHANGELOG.md generation from commit messages (commit history isn't consistent Conventional Commits).
- No automatic version bump of `main.py`'s `version="1.0.0"` string — CHANGELOG.md is the single source of truth for the release version; keeping `main.py` in sync (if desired) is a manual edit in the same PR.
- No npm/PyPI publishing — this repo isn't published as a package, the release is just a tagged GitHub Release with notes.
