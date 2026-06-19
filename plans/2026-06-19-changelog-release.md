# Changelog-Driven Release Automation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a hand-maintained `CHANGELOG.md` and a GitHub Actions workflow that automatically tags + publishes a GitHub Release whenever a new version section is pushed to `main`.

**Architecture:** `CHANGELOG.md` at repo root in Keep a Changelog format is the single source of truth for the release version. `.github/workflows/release.yml` triggers on push to `main` (only when `CHANGELOG.md` changes), extracts the top version header, skips if that version is already tagged, otherwise uses `taiki-e/parse-changelog` to pull the section body and `softprops/action-gh-release` to create the tag + release.

**Tech Stack:** GitHub Actions (`actions/checkout@v4`, `taiki-e/create-gh-release-action@v1`), bash/grep for header extraction.

> **Implementation note:** Task 2 below was written assuming `taiki-e/parse-changelog` could be used in a `uses:` step. It can't — it's a CLI tool, not a GitHub Action. The actual implementation splits this into two workflows (`tag-release.yml` + `publish-release.yml` using `taiki-e/create-gh-release-action@v1`); see `specs/2026-06-19-changelog-release-design.md` for the corrected design.

## Global Constraints

- Changelog format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) + [SemVer](https://semver.org/spec/v2.0.0.html) (from spec).
- Single repo-wide changelog/version — not split per component (from spec).
- Workflow only acts on `CHANGELOG.md` changes pushed to `main`; no auto version bump elsewhere, no package publishing (from spec).
- Release tag format: `vX.Y.Z` (`v` prefix + the version from the changelog header).
- If the top section is still `[Unreleased]` or its version is already tagged, the workflow must no-op without failing.

---

### Task 1: Create `CHANGELOG.md`

**Files:**
- Create: `CHANGELOG.md` (repo root)

**Interfaces:**
- Produces: a file with a top-level `# Changelog` heading, an `## [Unreleased]` section, and one dated version section `## [1.1.0] - 2026-06-19` directly below it. Task 3's extraction logic and Task 2's workflow both depend on this exact heading format: `## [X.Y.Z] - YYYY-MM-DD` (one space after `##`, version in square brackets, literal ` - `, ISO date).

- [ ] **Step 1: Write `CHANGELOG.md`**

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1.0] - 2026-06-19

### Security

- Bumped Python dependencies to close 24 known vulnerabilities reported by `pip-audit`, including `fastapi` 0.115.3 → 0.137.2, `starlette` 0.41.0 → 1.3.1, `python-multipart` 0.0.12 → 0.0.32, `Jinja2` 3.1.4 → 3.1.6, `python-dotenv` 1.0.1 → 1.2.2, `orjson` 3.10.10 → 3.11.6, `Pygments` 2.18.0 → 2.20.0, `idna` 3.10 → 3.18.
- Bumped `@docusaurus/*` packages 3.5.2 → 3.10.1 in `docs-docusaurus/`, closing all critical and high severity `npm audit` findings.
- Added `npm` `overrides` for `http-proxy-middleware`, `serialize-javascript`, and `uuid` to close moderate severity transitive vulnerabilities in the Docusaurus build toolchain.
- Patched the unmaintained `gray-matter` dependency (via `patch-package`) to use the `js-yaml` v4 API (`load`/`dump` instead of the removed `safeLoad`/`safeDump`), closing the remaining 22 moderate `npm audit` findings without breaking the Docusaurus build.
```

- [ ] **Step 2: Verify the heading format is machine-extractable**

Run:
```bash
grep -m1 -oP '(?<=^## \[)[0-9]+\.[0-9]+\.[0-9]+(?=\] - )' CHANGELOG.md
```
Expected output: `1.1.0`

This is the exact command Task 2's workflow uses — confirming it here means the workflow will work unmodified.

- [ ] **Step 3: Commit**

```bash
git add CHANGELOG.md
git commit -m "docs: add CHANGELOG.md"
```

---

### Task 2: Create the release workflow

**Files:**
- Create: `.github/workflows/release.yml`

**Interfaces:**
- Consumes: `CHANGELOG.md`'s heading format from Task 1 (`## [X.Y.Z] - YYYY-MM-DD`), via the same `grep -oP` pattern verified in Task 1 Step 2.
- Produces: a git tag `v$VERSION` and a GitHub Release, only on push to `main` when `CHANGELOG.md` changed and that version isn't already tagged.

- [ ] **Step 1: Write the workflow file**

```yaml
name: Release

on:
  push:
    branches: [main]
    paths: ['CHANGELOG.md']

permissions:
  contents: write

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Extract version from CHANGELOG.md
        id: extract
        run: |
          VERSION=$(grep -m1 -oP '(?<=^## \[)[0-9]+\.[0-9]+\.[0-9]+(?=\] - )' CHANGELOG.md || true)
          if [ -z "$VERSION" ]; then
            echo "No dated version section found at the top of CHANGELOG.md (still [Unreleased]?). Skipping release."
            echo "skip=true" >> "$GITHUB_OUTPUT"
            exit 0
          fi
          if git tag -l "v$VERSION" | grep -q "v$VERSION"; then
            echo "Tag v$VERSION already exists. Skipping release."
            echo "skip=true" >> "$GITHUB_OUTPUT"
            exit 0
          fi
          echo "version=$VERSION" >> "$GITHUB_OUTPUT"
          echo "skip=false" >> "$GITHUB_OUTPUT"

      - name: Parse release notes
        if: steps.extract.outputs.skip == 'false'
        id: parse
        uses: taiki-e/parse-changelog@v1
        with:
          changelog: CHANGELOG.md
          version: ${{ steps.extract.outputs.version }}

      - name: Create tag
        if: steps.extract.outputs.skip == 'false'
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git tag "v${{ steps.extract.outputs.version }}"
          git push origin "v${{ steps.extract.outputs.version }}"

      - name: Create GitHub Release
        if: steps.extract.outputs.skip == 'false'
        uses: softprops/action-gh-release@v2
        with:
          tag_name: v${{ steps.extract.outputs.version }}
          name: v${{ steps.extract.outputs.version }}
          body: ${{ steps.parse.outputs.changes }}
```

- [ ] **Step 2: Validate YAML syntax locally**

Run:
```bash
python -c "import yaml,sys; yaml.safe_load(open('.github/workflows/release.yml'))" && echo "OK"
```
Expected output: `OK`

(If `pyyaml` isn't installed locally, install it first with `pip install pyyaml`, or use `npx js-yaml .github/workflows/release.yml > /dev/null && echo OK` if Node is preferred.)

- [ ] **Step 3: Dry-run the extraction + skip logic against the real CHANGELOG.md**

Run:
```bash
VERSION=$(grep -m1 -oP '(?<=^## \[)[0-9]+\.[0-9]+\.[0-9]+(?=\] - )' CHANGELOG.md || true)
echo "Extracted: $VERSION"
git tag -l "v$VERSION"
```
Expected: `Extracted: 1.1.0` printed, and the `git tag -l` line prints nothing (no tag `v1.1.0` exists yet) — confirming the workflow would proceed to release on first run.

- [ ] **Step 4: Commit**

```bash
git add .github/workflows/release.yml
git commit -m "ci: add changelog-driven release workflow"
```

---

### Task 3: End-to-end verification on a test branch

**Files:**
- None created — this task only verifies Tasks 1-2 end to end before relying on them against `main`.

**Interfaces:**
- Consumes: `CHANGELOG.md` from Task 1, `.github/workflows/release.yml` from Task 2.
- Produces: a confirmed-working release on push, observed via the Actions tab and Releases page.

- [ ] **Step 1: Push a test branch with both files and open a throwaway PR-less push to confirm the workflow doesn't fire off-`main`**

Run:
```bash
git checkout -b test-release-workflow
git push -u origin test-release-workflow
```
Expected: no `Release` run appears under the repo's Actions tab (trigger is `branches: [main]` only).

- [ ] **Step 2: Merge to `main` (or push directly per repo convention) and watch the Actions tab**

After the push to `main` lands, open the repo's Actions tab.
Expected: a `Release` run appears, the `extract` step logs `skip=false` with `version=1.1.0`, and the run finishes green.

- [ ] **Step 3: Confirm the tag and release were created**

Run:
```bash
git fetch --tags
git tag -l "v1.1.0"
gh release view v1.1.0
```
Expected: `v1.1.0` printed by the tag list, and `gh release view` shows a release titled `v1.1.0` whose body matches the `### Security` bullets from `CHANGELOG.md`.

- [ ] **Step 4: Confirm idempotency — pushing an unrelated CHANGELOG.md typo fix doesn't re-release**

Make a trivial whitespace/typo fix anywhere in `CHANGELOG.md` that doesn't touch the top version header, push to `main`, and check the Actions tab.
Expected: the `Release` run's `extract` step logs `Tag v1.1.0 already exists. Skipping release.` and no new tag/release is created.

- [ ] **Step 5: Clean up the test branch**

```bash
git branch -d test-release-workflow
git push origin --delete test-release-workflow
```
