"""
Numba-accelerated Mandelbrot renderer.

pip install numba pillow numpy
"""

from PIL import Image

from mandelbrot_lib import mandelbrot, colorize

WIDTH, HEIGHT = 1920, 1080
MAX_ITER = 500

# Default full-set view
CENTER_X, CENTER_Y = -0.5, 0.0
ZOOM = 1.0  # half-height of the view in the complex plane


if __name__ == "__main__":
    print("Rendering...")
    escape = mandelbrot(WIDTH, HEIGHT, CENTER_X, CENTER_Y, ZOOM, MAX_ITER)

    img = Image.fromarray(colorize(escape, MAX_ITER), mode="RGB")
    img.save("mandelbrot.png")
    print("Saved mandelbrot.png")
