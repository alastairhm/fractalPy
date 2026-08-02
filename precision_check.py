"""
Render PNGs at deep zoom levels to visually check for float64
precision breakdown (artifacting, broken symmetry, static-like noise).

pip install numba numpy pillow
"""

import numpy as np
from numba import njit, prange
from PIL import Image

WIDTH, HEIGHT = 1920, 1080
MAX_ITER = 2000

CENTER_X, CENTER_Y = -0.743643887037151, 0.13182590420533

ZOOM_LEVELS = [1e-8, 1e-10, 1e-12, 1e-13, 1e-14]


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
                escape[row, col] = 0.0
            else:
                log_zn = np.log(zr * zr + zi * zi) / 2.0
                nu = np.log(log_zn / np.log(2.0)) / np.log(2.0)
                escape[row, col] = i + 1 - nu

    return escape


def colorize(escape, max_iter):
    norm = np.clip(escape / max_iter, 0, 1)
    r = (0.5 + 0.5 * np.cos(6.28318 * (norm * 3.0 + 0.0))) * 255
    g = (0.5 + 0.5 * np.cos(6.28318 * (norm * 3.0 + 0.33))) * 255
    b = (0.5 + 0.5 * np.cos(6.28318 * (norm * 3.0 + 0.67))) * 255
    rgb = np.stack([r, g, b], axis=-1).astype(np.uint8)
    rgb[escape == 0] = [0, 0, 0]
    return rgb


if __name__ == "__main__":
    for zoom in ZOOM_LEVELS:
        print(f"Rendering zoom={zoom:.0e}...")
        escape = mandelbrot(WIDTH, HEIGHT, CENTER_X, CENTER_Y, zoom, MAX_ITER)
        img = Image.fromarray(colorize(escape, MAX_ITER), mode="RGB")
        fname = f"zoom_{zoom:.0e}.png"
        img.save(fname)
        print(f"  saved {fname}")
