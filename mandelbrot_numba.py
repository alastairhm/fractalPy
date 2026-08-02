"""
Numba-accelerated Mandelbrot renderer.

pip install numba pillow numpy
"""

import argparse

from PIL import Image

from mandelbrot_lib import colorize, mandelbrot

WIDTH, HEIGHT = 1920, 1080
MAX_ITER = 500

# Default full-set view
CENTER_X, CENTER_Y = -0.5, 0.0
ZOOM = 1.0  # half-height of the view in the complex plane

OUTPUT = "mandelbrot.png"


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--width", type=int, default=WIDTH)
    parser.add_argument("--height", type=int, default=HEIGHT)
    parser.add_argument("--max-iter", type=int, default=MAX_ITER)
    parser.add_argument("--center-x", type=float, default=CENTER_X)
    parser.add_argument("--center-y", type=float, default=CENTER_Y)
    parser.add_argument(
        "--zoom", type=float, default=ZOOM, help="half-height of the view in the complex plane"
    )
    parser.add_argument("--output", default=OUTPUT)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    print("Rendering...")
    escape = mandelbrot(
        args.width, args.height, args.center_x, args.center_y, args.zoom, args.max_iter
    )

    img = Image.fromarray(colorize(escape, args.max_iter), mode="RGB")
    img.save(args.output)
    print(f"Saved {args.output}")
