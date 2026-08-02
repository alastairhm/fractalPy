"""
Benchmark: render time across zoom levels and iteration counts.

pip install numba numpy
"""

import time

from mandelbrot_lib import mandelbrot_raw as mandelbrot

WIDTH, HEIGHT = 1920, 1080

# A point near the boundary, good for testing deep zooms
CENTER_X, CENTER_Y = -0.743643887037151, 0.13182590420533

ZOOM_LEVELS = [1.0, 1e-2, 1e-4, 1e-6, 1e-8, 1e-10, 1e-12, 1e-14]
ITER_LEVELS = [500, 1000, 2000, 4000]


if __name__ == "__main__":
    # warm up JIT compilation before timing anything
    mandelbrot(64, 64, CENTER_X, CENTER_Y, 1.0, 50)

    print(f"{'zoom':>10} | " + " | ".join(f"iter={it:>5}" for it in ITER_LEVELS))
    print("-" * (13 + 14 * len(ITER_LEVELS)))

    for zoom in ZOOM_LEVELS:
        row = [f"{zoom:>10.0e}"]
        for max_iter in ITER_LEVELS:
            start = time.perf_counter()
            mandelbrot(WIDTH, HEIGHT, CENTER_X, CENTER_Y, zoom, max_iter)
            elapsed = time.perf_counter() - start
            row.append(f"{elapsed:>10.3f}s")
        print(" | ".join(row))
