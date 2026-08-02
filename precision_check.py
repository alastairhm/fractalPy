"""
Render PNGs at deep zoom levels to visually check for float64
precision breakdown (artifacting, broken symmetry, static-like noise).

pip install numba numpy pillow
"""

import argparse

from PIL import Image

from mandelbrot_lib import colorize, mandelbrot

WIDTH, HEIGHT = 1920, 1080
MAX_ITER = 2000

CENTER_X, CENTER_Y = -0.743643887037151, 0.13182590420533

ZOOM_LEVELS = [1e-8, 1e-10, 1e-12, 1e-13, 1e-14]


def float_list(text):
    return [float(item) for item in text.split(",")]


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--width", type=int, default=WIDTH)
    parser.add_argument("--height", type=int, default=HEIGHT)
    parser.add_argument("--max-iter", type=int, default=MAX_ITER)
    parser.add_argument("--center-x", type=float, default=CENTER_X)
    parser.add_argument("--center-y", type=float, default=CENTER_Y)
    parser.add_argument(
        "--zoom-levels", type=float_list, default=ZOOM_LEVELS, help="comma-separated zoom values"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    for zoom in args.zoom_levels:
        print(f"Rendering zoom={zoom:.0e}...")
        escape = mandelbrot(
            args.width, args.height, args.center_x, args.center_y, zoom, args.max_iter
        )
        img = Image.fromarray(colorize(escape, args.max_iter), mode="RGB")
        fname = f"zoom_{zoom:.0e}.png"
        img.save(fname)
        print(f"  saved {fname}")
