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

### Fixed

- Replaced the release workflow's invalid use of `taiki-e/parse-changelog` (a CLI tool, not a GitHub Action) with `taiki-e/create-gh-release-action@v1`, which parses the changelog itself and creates the tag + GitHub Release in a single workflow run on push to `main`.
