"""
Benchmark: render time across zoom levels and iteration counts.

pip install numba numpy
"""

import argparse
import time

from mandelbrot_lib import mandelbrot_raw as mandelbrot

WIDTH, HEIGHT = 1920, 1080

# A point near the boundary, good for testing deep zooms
CENTER_X, CENTER_Y = -0.743643887037151, 0.13182590420533

ZOOM_LEVELS = [1.0, 1e-2, 1e-4, 1e-6, 1e-8, 1e-10, 1e-12, 1e-14]
ITER_LEVELS = [500, 1000, 2000, 4000]


def float_list(text):
    return [float(item) for item in text.split(",")]


def int_list(text):
    return [int(item) for item in text.split(",")]


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--width", type=int, default=WIDTH)
    parser.add_argument("--height", type=int, default=HEIGHT)
    parser.add_argument("--center-x", type=float, default=CENTER_X)
    parser.add_argument("--center-y", type=float, default=CENTER_Y)
    parser.add_argument(
        "--zoom-levels", type=float_list, default=ZOOM_LEVELS, help="comma-separated zoom values"
    )
    parser.add_argument(
        "--iter-levels",
        type=int_list,
        default=ITER_LEVELS,
        help="comma-separated max-iteration values",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    # warm up JIT compilation before timing anything
    mandelbrot(64, 64, args.center_x, args.center_y, 1.0, 50)

    print(f"{'zoom':>10} | " + " | ".join(f"iter={it:>5}" for it in args.iter_levels))
    print("-" * (13 + 14 * len(args.iter_levels)))

    for zoom in args.zoom_levels:
        row = [f"{zoom:>10.0e}"]
        for max_iter in args.iter_levels:
            start = time.perf_counter()
            mandelbrot(args.width, args.height, args.center_x, args.center_y, zoom, max_iter)
            elapsed = time.perf_counter() - start
            row.append(f"{elapsed:>10.3f}s")
        print(" | ".join(row))
