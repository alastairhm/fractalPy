"""
Benchmark: render time across zoom levels and iteration counts.

pip install numba numpy
"""

import time
import numpy as np
from numba import njit, prange

WIDTH, HEIGHT = 1920, 1080

# A point near the boundary, good for testing deep zooms
CENTER_X, CENTER_Y = -0.743643887037151, 0.13182590420533

ZOOM_LEVELS = [1.0, 1e-2, 1e-4, 1e-6, 1e-8, 1e-10, 1e-12, 1e-14]
ITER_LEVELS = [500, 1000, 2000, 4000]


@njit(parallel=True, fastmath=True, cache=True)
def mandelbrot(width, height, cx, cy, zoom, max_iter):
    aspect = width / height
    x_min, x_max = cx - zoom * aspect, cx + zoom * aspect
    y_min, y_max = cy - zoom, cy + zoom

    escape = np.zeros((height, width), dtype=np.float64)

    for row in prange(height):
        y = y_min + (y_max - y_min) * row / (height - 1)
        for col in range(width):
            x = x_min + (x_max - x_min) * col / (width - 1)

            zr, zi = 0.0, 0.0
            i = 0
            while zr * zr + zi * zi <= 4.0 and i < max_iter:
                zr, zi = zr * zr - zi * zi + x, 2.0 * zr * zi + y
                i += 1

            escape[row, col] = 0.0 if i == max_iter else i

    return escape


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

