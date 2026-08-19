#!/usr/bin/env python3
from pathlib import Path
from PIL import Image
import colorsys

ROOT = Path(__file__).parent / "images"


def rgb_hsv(r, g, b):
    return colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)


def to_ice(r, g, b, a, sat=0.38, val=None):
    h, s, v = rgb_hsv(r, g, b)
    nv = val if val is not None else min(1.0, max(v, 0.72))
    nr, ng, nb = colorsys.hsv_to_rgb(0.57, sat, nv)
    return int(nr * 255), int(ng * 255), int(nb * 255), a


def is_warm(h, s, v):
    if v < 0.12:
        return False
    return (h <= 0.12 or h >= 0.82) and s >= 0.06


def clean_balloon(path):
    img = Image.open(path).convert("RGBA")
    px = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a < 8:
                continue
            hv, s, v = rgb_hsv(r, g, b)
            # pale pink / cream tile -> transparent
            if s < 0.22 and v > 0.88 and r > 220 and g > 200:
                px[x, y] = (0, 0, 0, 0)
                continue
            if is_warm(hv, s, v):
                px[x, y] = to_ice(r, g, b, a, sat=min(0.42, s * 0.8), val=min(1.0, v * 1.02))
    img.save(path)
    print("cleaned", path.name)


def clean_decorate(path):
    img = Image.open(path).convert("RGBA")
    px = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a < 8:
                continue
            hv, s, v = rgb_hsv(r, g, b)
            if is_warm(hv, s, v) or (r > g + 20 and r > b + 10 and v > 0.4):
                # outer wave a bit deeper blue, inner fill lighter
                if r > 220 and g < 180:
                    px[x, y] = to_ice(r, g, b, a, sat=0.28, val=0.93)
                else:
                    px[x, y] = to_ice(r, g, b, a, sat=0.45, val=0.82)
    img.save(path)
    print("cleaned", path.name)


def clean_hearts(path):
    img = Image.open(path).convert("RGBA")
    px = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a < 8:
                continue
            hv, s, v = rgb_hsv(r, g, b)
            if is_warm(hv, s, v) or (r > 160 and r > g + 15 and r > b):
                px[x, y] = to_ice(r, g, b, a, sat=0.40, val=min(0.95, max(v, 0.7)))
    img.save(path)
    print("cleaned", path.name)


def clean_flag(path):
    img = Image.open(path).convert("RGBA")
    px = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a < 8:
                continue
            hv, s, v = rgb_hsv(r, g, b)
            if is_warm(hv, s, v):
                px[x, y] = to_ice(r, g, b, a, sat=0.32, val=0.90)
    img.save(path)
    print("cleaned", path.name)


if __name__ == "__main__":
    clean_balloon(ROOT / "balloon1.png")
    clean_balloon(ROOT / "balloon2.png")
    clean_decorate(ROOT / "decorate.png")
    clean_hearts(ROOT / "heart_letter.png")
    clean_flag(ROOT / "1.png")
