# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Linked `CHANGELOG.md` and the GitHub Releases page from the README and the Docusaurus site footer.

### Security

- Bumped `pydantic-settings` 2.14.1 → 2.14.2 in `requirements.txt`, closing a moderate severity advisory reported by Dependabot.
- Added `npm` `overrides` in `docs-docusaurus/package.json` for `js-yaml` (→ 4.3.1), `nanoid` (→ 3.3.18), `postcss` (→ 8.5.23), `brace-expansion` (→ 1.1.18), `fast-uri` (→ 3.1.5), `body-parser` (→ 1.20.6), `webpack-dev-server` (→ 5.2.6), `shell-quote` (→ 1.9.0), and `svgo` (→ 3.3.4), closing 12 high/medium severity `npm audit` findings in the Docusaurus build toolchain. Verified `npm run build` still succeeds.
- `image-size` (pulled in transitively by `@docusaurus/mdx-loader`) remains on the vulnerable `<=2.0.2` line for two DoS advisories (GHSA-w3rx-r6r6-pgpr, GHSA-5p2g-fcmc-qvqq); no patched release exists upstream yet. Risk is limited since `image-size` only runs at docs build time against trusted repo content, not at runtime against user input. Tracked for a follow-up bump once a fix is published.
- Bumped `anyio` 4.14.0 → 4.14.2 in `requirements.txt`, closing one critical (CVE-2026-63374, TLS certificate spoofing via IDNA 2003 host encoding) and two additional Dependabot advisories.
- `image-size` fix landed upstream (2.0.3): added `npm` override pinning it to 2.0.4 in `docs-docusaurus/package.json`, closing the two DoS advisories noted above.
- Bumped further `npm` `overrides` in `docs-docusaurus/package.json`: `js-yaml` (→ 4.3.2), `fast-uri` (→ 3.1.6), `svgo` (→ 3.3.5), and added new overrides for `browserslist` (→ 4.28.7), `baseline-browser-mapping` (→ 2.11.0), `colord` (→ 2.9.4), `joi` (→ 17.13.6), and `qs` (→ 6.16.0), closing 13 high/medium/low severity Dependabot alerts in the Docusaurus build toolchain. Verified `npm run build` still succeeds with 0 `npm audit` findings.

## [1.1.0] - 2026-06-19

### Security

- Bumped Python dependencies to close 24 known vulnerabilities reported by `pip-audit`, including `fastapi` 0.115.3 → 0.137.2, `starlette` 0.41.0 → 1.3.1, `python-multipart` 0.0.12 → 0.0.32, `Jinja2` 3.1.4 → 3.1.6, `python-dotenv` 1.0.1 → 1.2.2, `orjson` 3.10.10 → 3.11.6, `Pygments` 2.18.0 → 2.20.0, `idna` 3.10 → 3.18.
- Bumped `@docusaurus/*` packages 3.5.2 → 3.10.1 in `docs-docusaurus/`, closing all critical and high severity `npm audit` findings.
- Added `npm` `overrides` for `http-proxy-middleware`, `serialize-javascript`, and `uuid` to close moderate severity transitive vulnerabilities in the Docusaurus build toolchain.
- Patched the unmaintained `gray-matter` dependency (via `patch-package`) to use the `js-yaml` v4 API (`load`/`dump` instead of the removed `safeLoad`/`safeDump`), closing the remaining 22 moderate `npm audit` findings without breaking the Docusaurus build.

### Fixed

- Replaced the release workflow's invalid use of `taiki-e/parse-changelog` (a CLI tool, not a GitHub Action) with `taiki-e/create-gh-release-action@v1`, which parses the changelog itself and creates the tag + GitHub Release in a single workflow run on push to `main`.
