# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A small, dependency-light Mandelbrot set renderer accelerated with Numba. Not a package (no `setup.py`/`pyproject.toml`) — three standalone scripts plus a shared `mandelbrot_lib.py` module with the core kernel(s) and coloring.

## Environment

A virtualenv already exists at `fractal-env/` (Python 3.10.12). Use it directly rather than creating a new one:

```
./fractal-env/bin/python <script>.py
./fractal-env/bin/pip install <pkg>
```

Dependencies are pinned in `requirements.txt` (`numpy`, `numba`, `pillow`); install with `./fractal-env/bin/pip install -r requirements.txt`. `llvmlite` (0.48.0) comes in as a transitive dependency of `numba`.

## Scripts

- `mandelbrot_lib.py` — shared library: `mandelbrot()` (smoothed kernel) and `mandelbrot_raw()` (unsmoothed, for benchmarking) escape-time kernels, plus `colorize()`. All three scripts below import from here rather than defining their own copies.
- `mandelbrot_numba.py` — renders a single full-set view to `mandelbrot.png`. Edit `WIDTH`, `HEIGHT`, `MAX_ITER`, `CENTER_X`, `CENTER_Y`, `ZOOM` constants at the top to change the view.
- `benchmark.py` — times the render across a grid of zoom levels (`ZOOM_LEVELS`) and iteration counts (`ITER_LEVELS`), printing a table. Uses `mandelbrot_raw` (non-smoothed escape count, no log/coloring overhead) since it's measuring raw kernel speed.
- `precision_check.py` — renders PNGs at a sequence of deep zoom levels (down to 1e-14) to visually inspect for float64 precision breakdown (artifacting, broken symmetry, static-like noise). This is the point at which double precision runs out for Mandelbrot rendering — a known limit, not a bug to fix in `zr`/`zi` arithmetic.

Run any script directly, e.g. `./fractal-env/bin/python mandelbrot_numba.py`. There is no test suite; validation is visual (inspect the output PNG).

## Git workflow

- Never push directly to `master`. Do all work on a feature branch and open a PR (`gh pr create`).
- Every push must include an updated `CHANGELOG.md` entry describing the change.

## Architecture notes

- `mandelbrot()` and `mandelbrot_raw()` in `mandelbrot_lib.py` share the same escape-time loop and coordinate mapping; `mandelbrot_raw()` intentionally skips smoothing (used only by `benchmark.py`, to measure raw kernel speed without log/coloring overhead). If you change the escape-time algorithm (e.g. adjust the bailout radius or parallelization), update both functions consistently.
- Both kernels are `@njit(parallel=True, fastmath=True, cache=True)`. `cache=True` means Numba caches compiled machine code in `__pycache__/*.nbi`/`*.nbc` files — delete `__pycache__` if you suspect a stale compiled kernel isn't picking up source changes (rare, but `fastmath`/signature changes can be finicky with the cache).
- Coordinate mapping: the view window is derived from `(cx, cy, zoom)` plus an `aspect = width / height` correction, giving `x_min/x_max/y_min/y_max`. `zoom` is the half-height of the view in the complex plane, so smaller `zoom` = deeper zoom.
- Smooth coloring (`mandelbrot()` + `colorize()`, used by `mandelbrot_numba.py` and `precision_check.py`) uses the continuous (normalized) iteration count formula (`i + 1 - nu`) to avoid banding, then `colorize()` maps that through a cosine-based periodic RGB gradient. Points that never escape (`i == max_iter`) are marked `0.0` and forced to pure black in `colorize()`.
