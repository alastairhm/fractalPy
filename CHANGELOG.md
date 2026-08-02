# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
- Git repository initialized, with `.gitignore`, `README.md`, and this changelog.
- `CLAUDE.md` for guidance when working in this repo with Claude Code.
- `LICENSE` (MIT) and a corresponding license badge in the README.
- README screenshot of a rendered Mandelbrot set (`docs/screenshot.png`).

### Changed
- Documented git workflow in `CLAUDE.md`: changes go on a feature branch with a PR (no direct pushes to `master`), and `CHANGELOG.md` is updated on every push.

## [0.1.0] - 2026-08-02

### Added
- `mandelbrot_numba.py` — renders a single full-set Mandelbrot view to `mandelbrot.png`, with smooth (continuous) iteration coloring.
- `benchmark.py` — times the render kernel across a grid of zoom levels and iteration counts.
- `precision_check.py` — renders PNGs at deep zoom levels to visually check for float64 precision breakdown.
