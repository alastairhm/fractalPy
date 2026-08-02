"""
Shared Mandelbrot kernel and coloring, used by mandelbrot_numba.py,
precision_check.py, and benchmark.py.
"""

import numpy as np
from numba import njit, prange


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

            if i == max_iter:
                escape[row, col] = 0.0  # inside the set -> stays black
            else:
                # smooth (continuous) iteration count to avoid banding
                log_zn = np.log(zr * zr + zi * zi) / 2.0
                nu = np.log(log_zn / np.log(2.0)) / np.log(2.0)
                escape[row, col] = i + 1 - nu

    return escape


@njit(parallel=True, fastmath=True, cache=True)
def mandelbrot_raw(width, height, cx, cy, zoom, max_iter):
    """Unsmoothed escape-time kernel, for measuring raw kernel speed."""
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


def colorize(escape, max_iter):
    """Map smooth escape values to an RGB image using a simple gradient."""
    norm = np.clip(escape / max_iter, 0, 1)

    # simple periodic gradient for that swirly banded-but-smooth look
    r = (0.5 + 0.5 * np.cos(6.28318 * (norm * 3.0 + 0.0))) * 255
    g = (0.5 + 0.5 * np.cos(6.28318 * (norm * 3.0 + 0.33))) * 255
    b = (0.5 + 0.5 * np.cos(6.28318 * (norm * 3.0 + 0.67))) * 255

    rgb = np.stack([r, g, b], axis=-1).astype(np.uint8)
    rgb[escape == 0] = [0, 0, 0]  # points inside the set: pure black
    return rgb
