"""
Render PNGs at deep zoom levels to visually check for float64
precision breakdown (artifacting, broken symmetry, static-like noise).

pip install numba numpy pillow
"""

from PIL import Image

from mandelbrot_lib import mandelbrot, colorize

WIDTH, HEIGHT = 1920, 1080
MAX_ITER = 2000

CENTER_X, CENTER_Y = -0.743643887037151, 0.13182590420533

ZOOM_LEVELS = [1e-8, 1e-10, 1e-12, 1e-13, 1e-14]


if __name__ == "__main__":
    for zoom in ZOOM_LEVELS:
        print(f"Rendering zoom={zoom:.0e}...")
        escape = mandelbrot(WIDTH, HEIGHT, CENTER_X, CENTER_Y, zoom, MAX_ITER)
        img = Image.fromarray(colorize(escape, MAX_ITER), mode="RGB")
        fname = f"zoom_{zoom:.0e}.png"
        img.save(fname)
        print(f"  saved {fname}")
