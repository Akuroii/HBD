#!/usr/bin/env python3
"""Shift pink/coral pixels toward the ice-blue palette from the reference art."""
from pathlib import Path
from PIL import Image
import colorsys

ROOT = Path(__file__).parent / "images"

# Files that are mostly pink fills + navy outlines
TARGETS = [
    "1.png",
    "balloon1.png",
    "balloon2.png",
    "hat.png",
    "decorate.png",
    "heart.png",
    "heart_letter.png",
]


def is_pinkish(h, s, v):
    if s < 0.08 or v < 0.18:
        return False
    # reds / magentas / peaches
    return h <= 0.10 or h >= 0.88


def recolor_pixel(r, g, b, a):
    if a < 8:
        return r, g, b, a
    h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)

    # Knock out the leftover pale pink tile behind balloons
    if a > 200 and s < 0.18 and v > 0.90 and (h <= 0.12 or h >= 0.85 or g >= r * 0.92):
        if r > 230 and g > 210 and b > 210:
            return 0, 0, 0, 0

    if is_pinkish(h, s, v):
        # ice / sky blue around 205 deg
        new_h = 0.57
        new_s = min(max(s * 0.72, 0.22), 0.58)
        new_v = min(1.0, v * 1.04 if v < 0.92 else v)
        nr, ng, nb = colorsys.hsv_to_rgb(new_h, new_s, new_v)
        return int(nr * 255), int(ng * 255), int(nb * 255), a

    return r, g, b, a


def process(name):
    src = ROOT / name
    img = Image.open(src).convert("RGBA")
    px = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            px[x, y] = recolor_pixel(*px[x, y])
    img.save(src)
    print(f"recolored {name} {w}x{h}")


def make_heart():
    """Clean ice-blue heart used in the letter."""
    size = 64
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    px = img.load()
    cx, cy = size / 2, size / 2 + 4
    for y in range(size):
        for x in range(size):
            nx = (x - cx) / (size * 0.42)
            ny = (y - cy) / (size * 0.42)
            # classic heart implicit equation
            val = (nx * nx + ny * ny - 1) ** 3 - nx * nx * ny * ny * ny
            if val <= 0:
                # highlight toward top-left
                t = max(0.0, min(1.0, (x + (size - y)) / (size * 1.6)))
                r = int(90 + 90 * t)
                g = int(170 + 55 * t)
                b = int(230 + 20 * t)
                px[x, y] = (r, g, b, 255)
    img.save(ROOT / "heart.png")
    print("drew heart.png")


if __name__ == "__main__":
    for name in TARGETS:
        if name == "heart.png":
            continue
        process(name)
    make_heart()
