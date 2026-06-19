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

- Trigger: `push` to `main`, `paths: ['CHANGELOG.md']`.
- Permissions: `contents: write` (to push tags and create releases).
- Steps:
  1. `actions/checkout@v4` with `fetch-depth: 0` (full history, so existing tags are visible) and `fetch-tags: true`.
  2. Extract the first version header from `CHANGELOG.md` (first line matching `## [X.Y.Z] - `), e.g. via `grep -m1 -oP '(?<=^## \[)[0-9]+\.[0-9]+\.[0-9]+(?=\])' CHANGELOG.md`. Set as step output `version`.
  3. If `version` output is empty (e.g. top section is still `[Unreleased]`), skip the rest of the job — nothing to release.
  4. Check whether tag `v$version` already exists (`git tag -l`). If it does, skip the rest — this version was already released (e.g. unrelated CHANGELOG.md edit, like fixing a typo in an old entry, shouldn't trigger a re-release).
  5. Use `taiki-e/parse-changelog@v1` to extract that version's section body as release notes.
  6. Create and push git tag `v$version` pointing at the triggering commit.
  7. `softprops/action-gh-release@v2` with `tag_name: v$version`, `name: v$version`, `body` = parsed notes — creates the GitHub Release.

## Out of scope

- No automatic CHANGELOG.md generation from commit messages (commit history isn't consistent Conventional Commits).
- No automatic version bump of `main.py`'s `version="1.0.0"` string — CHANGELOG.md is the single source of truth for the release version; keeping `main.py` in sync (if desired) is a manual edit in the same PR.
- No npm/PyPI publishing — this repo isn't published as a package, the release is just a tagged GitHub Release with notes.
