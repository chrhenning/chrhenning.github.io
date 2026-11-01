"""Five reasons to care about uncertainty, one panel each, built from images in this folder.

Run: python why_care.py  (requires numpy, matplotlib, pillow)
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from common import INK, INK2, SURFACE, setup_style

HERE = Path(__file__).parent
OUT = HERE / "why-care.png"

PANELS = [
    ("A human decides", "“20% rain” means one thing for a wedding,\nanother for a walk",
     ["wedding_vs_walk.jpeg"]),
    ("A point estimate is not enough", "Several plausible outcomes\nand costly tail risks",
     ["Blank_Fork.png", "09_tail_risk.png"]),
    ("We can choose not to decide yet", "Unsure cases go to a human",
     ["phone_screen_dust.jpeg"]),
    ("We can ask for the right data", "Query where new data is most useful",
     ["10_active_learning.png"]),
    ("It feeds further computation", "Sensor fusion weighs each input\nby its uncertainty",
     ["11_sensor_fusion.png"]),
]


def show(ax, name):
    ax.imshow(np.asarray(Image.open(HERE / name).convert("RGB")))
    ax.set_anchor("C")
    ax.axis("off")


def main():
    setup_style()
    fig = plt.figure(figsize=(12, 8.6), facecolor=SURFACE)
    w, h = 0.29, 0.31
    lefts = [0.03, 0.355, 0.68, 0.19, 0.515]
    bottoms = [0.56, 0.56, 0.56, 0.08, 0.08]
    for i, ((title, caption, images), x, y) in enumerate(zip(PANELS, lefts, bottoms), 1):
        fig.text(x + w / 2, y + h + 0.055, f"{i}. {title}", ha="center", va="bottom",
                 fontsize=15, weight="bold", color=INK)
        fig.text(x + w / 2, y - 0.015, caption, ha="center", va="top", fontsize=12.5,
                 color=INK2, linespacing=1.3)
        if len(images) == 1:
            show(fig.add_axes((x, y, w, h + 0.04)), images[0])
        else:
            show(fig.add_axes((x, y + h / 2 + 0.01, w, h / 2 + 0.03)), images[0])
            show(fig.add_axes((x, y, w, h / 2)), images[1])
    fig.savefig(OUT, dpi=150, facecolor=SURFACE)


if __name__ == "__main__":
    main()
