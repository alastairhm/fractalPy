# fractalPy

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A small, dependency-light Mandelbrot set renderer accelerated with [Numba](https://numba.pydata.org/).

## Setup

```
python3 -m venv fractal-env
./fractal-env/bin/pip install numpy numba pillow
```

## Usage

Render a single full-set view to `mandelbrot.png`:

```
./fractal-env/bin/python mandelbrot_numba.py
```

Edit the `WIDTH`, `HEIGHT`, `MAX_ITER`, `CENTER_X`, `CENTER_Y`, `ZOOM` constants at the top of the script to change the view.

Benchmark render time across a grid of zoom levels and iteration counts:

```
./fractal-env/bin/python benchmark.py
```

Render PNGs at a sequence of deep zoom levels to visually check for float64 precision breakdown:

```
./fractal-env/bin/python precision_check.py
```

## Notes

- The Mandelbrot kernel is JIT-compiled with `@njit(parallel=True, fastmath=True, cache=True)`; compiled code is cached under `__pycache__/`.
- Double-precision (float64) arithmetic limits how deep you can zoom before artifacting appears — see the output of `precision_check.py`.
