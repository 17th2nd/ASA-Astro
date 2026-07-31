"""Generate a deterministic synthetic RGB observation fixture with no third-party data."""

from __future__ import annotations

import math
from pathlib import Path


WIDTH = 96
HEIGHT = 96


def _ellipse(x: int, y: int, cx: float, cy: float, rx: float, ry: float) -> float:
    radius = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
    return max(0.0, 1.0 - radius)


def _gaussian(x: int, y: int, cx: float, cy: float, sigma: float) -> float:
    radius_squared = (x - cx) ** 2 + (y - cy) ** 2
    return math.exp(-radius_squared / (2 * sigma**2))


def create_fixture(path: Path) -> Path:
    """Write a byte-stable P6 PPM containing only synthetic image-space structures."""

    pixels = bytearray()
    stars = ((12.0, 14.0, 1.15), (81.0, 17.0, 1.0), (76.0, 78.0, 1.2))
    for y in range(HEIGHT):
        for x in range(WIDTH):
            base = 7 + ((x + 2 * y) % 3)
            red = green = blue = float(base)

            primary = _ellipse(x, y, 48.0, 49.0, 27.0, 16.0)
            if primary:
                contribution = 118 * primary**1.7
                red += contribution * 0.72
                green += contribution * 0.86
                blue += contribution

            companion = _ellipse(x, y, 79.0, 51.0, 6.0, 4.0)
            if companion:
                contribution = 92 * companion**1.4
                red += contribution
                green += contribution * 0.82
                blue += contribution * 0.66

            background_extended = _ellipse(x, y, 18.0, 76.0, 8.0, 5.0)
            if background_extended:
                contribution = 49 * background_extended**1.2
                red += contribution * 0.75
                green += contribution
                blue += contribution * 0.9

            for star_x, star_y, sigma in stars:
                contribution = 252 * _gaussian(x, y, star_x, star_y, sigma)
                red = max(red, contribution)
                green = max(green, contribution)
                blue = max(blue, contribution)

            spike_core = 238 * _gaussian(x, y, 34.0, 21.0, 0.9)
            horizontal_spike = 100 * math.exp(-abs(x - 34) / 6) if abs(y - 21) <= 0 else 0
            vertical_spike = 100 * math.exp(-abs(y - 21) / 6) if abs(x - 34) <= 0 else 0
            spike = max(spike_core, horizontal_spike, vertical_spike)
            red = max(red, spike)
            green = max(green, spike)
            blue = max(blue, spike)

            if primary and 35 <= x <= 61 and 46 <= y <= 49:
                red -= 52
                green -= 52
                blue -= 52

            pixels.extend(
                (
                    max(0, min(255, int(round(red)))),
                    max(0, min(255, int(round(green)))),
                    max(0, min(255, int(round(blue)))),
                )
            )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(f"P6\n{WIDTH} {HEIGHT}\n255\n".encode("ascii") + bytes(pixels))
    return path


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    arguments = parser.parse_args()
    create_fixture(arguments.output)
