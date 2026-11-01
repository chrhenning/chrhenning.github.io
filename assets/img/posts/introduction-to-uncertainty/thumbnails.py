"""The blog thumbnail and the social preview: the lane-split photo next to its sketch.

Run: python thumbnails.py  (requires pillow; run 00_lane_split_sketch.py first)
"""

from pathlib import Path

from PIL import Image

from common import SURFACE

HERE = Path(__file__).parent
GAP = 0.02


def combine(width, height, crops):
    """Each image is cropped to (top, bottom) fractions first, so both fill the frame."""
    gap = round(GAP * width)
    panel_w = (width - gap) // 2
    out = Image.new("RGB", (width, height), SURFACE)
    for i, (name, (top, bottom)) in enumerate(crops.items()):
        im = Image.open(HERE / name).convert("RGB")
        im = im.crop((0, round(top * im.height), im.width, round(bottom * im.height)))
        # Fill the panel and cut the overhang evenly from the sides.
        scale = max(panel_w / im.width, height / im.height)
        im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
        left = (im.width - panel_w) // 2
        im = im.crop((left, 0, left + panel_w, height))
        out.paste(im, (i * (panel_w + gap), 0))
    return out


combine(480, 346, {"lane-split.jpg": (0, 1), "00_lane_split_sketch.png": (0, 1)}).save(
    HERE / "lane-split-thumb.jpg", quality=90)
# The social preview is wider, so both images lose their top: the sky and the far ends of the roads.
combine(1200, 630, {"lane-split.jpg": (0.2, 0.85), "00_lane_split_sketch.png": (0.25, 0.99)}).save(
    HERE / "lane-split-og.jpg", quality=90)
