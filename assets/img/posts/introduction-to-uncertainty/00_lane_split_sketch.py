"""A top-down sketch of the lane split, with the cross section that defines the input x.

Run: python 00_lane_split_sketch.py  (requires numpy, matplotlib)
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from matplotlib.path import Path

from common import INK2, OFF_ROAD, SURFACE, TRUTH, save, setup_style

ROAD_GREY = "#bab8b2"
Y_SPLIT, Y_TOP, Y_CROSS = 3.4, 9.3, 1.4
BEND = 0.12


# Each branch is two lanes of constant width around a curved divider. Both branches start on the
# middle lane, so the divider between them appears where their inner edges cross.
def divider(sign, t):
    return np.stack([sign * (0.5 + BEND * t**2), Y_SPLIT + t])


def offset(sign, t, lanes):
    """The line `lanes` lane widths outward from the branch's divider."""
    normal = np.stack([sign * np.ones_like(t), -2 * BEND * t]) / np.hypot(1, 2 * BEND * t)
    return divider(sign, t) + lanes * normal


def with_straight(curve):
    return np.concatenate([[curve[0][0]], curve[0]]), np.concatenate([[0], curve[1]])


ts = np.linspace(0, Y_TOP - Y_SPLIT + 1, 400)
t_nose = ts[np.argmax(offset(1, ts, -1)[0] > 0)]
ts_gore = np.linspace(t_nose, ts[-1], 300)

setup_style()
fig, ax = plt.subplots(figsize=(4.4, 6.4), facecolor=SURFACE)
ax.set_facecolor(OFF_ROAD)
ax.set_aspect("equal")
ax.set_xlim(-3.2, 3.2)
ax.set_ylim(0, Y_TOP)
ax.set_xticks([])
ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)

edges = [with_straight(offset(sign, ts, 1)) for sign in (-1, 1)]
ax.fill(np.concatenate([edges[0][0], edges[1][0][::-1]]),
        np.concatenate([edges[0][1], edges[1][1][::-1]]), color=ROAD_GREY, lw=0, zorder=0)
inner = [offset(sign, ts_gore, -1) for sign in (-1, 1)]
ax.fill(np.concatenate([inner[0][0], inner[1][0][::-1]]),
        np.concatenate([inner[0][1], inner[1][1][::-1]]), color=OFF_ROAD, lw=0, zorder=1)

for xs, ys in edges + inner:
    ax.plot(xs, ys, color="white", lw=2.5, zorder=2)
for sign in (-1, 1):
    ax.plot(*with_straight(divider(sign, ts)), color="white", lw=2, ls=(0, (4, 4)), zorder=2)

# Each lane's choices, drawn in the colour of the truth p*(y|x) in the other figures.
t_end = np.linspace(0, 3.2, 100)
for sign, lanes in ((-1, 0.5), (-1, -0.5), (1, -0.5), (1, 0.5)):
    xs, ys = with_straight(offset(sign, t_end, lanes))
    verts = np.column_stack([xs, np.maximum(ys, Y_CROSS + 0.7)])
    ax.add_patch(FancyArrowPatch(path=Path(verts), arrowstyle="-|>", mutation_scale=16,
                                 color=TRUTH, lw=2.2, zorder=3))

ax.add_patch(FancyBboxPatch((-0.28, 0.35), 0.56, 0.85, boxstyle="round,pad=0,rounding_size=0.12",
                            color=INK2, zorder=3))
ax.plot([-1.5, 1.5], [Y_CROSS, Y_CROSS], color=INK2, lw=1.6, zorder=4)
for x, label in ((-1, "left"), (0, "middle"), (1, "right")):
    ax.plot([x, x], [Y_CROSS - 0.08, Y_CROSS + 0.08], color=INK2, lw=1.6, zorder=4)
    ax.text(x, Y_CROSS + 0.18, label, fontsize=12, color=INK2, ha="center", va="bottom", zorder=4,
            bbox=dict(fc=ROAD_GREY, ec="none", pad=1))
ax.text(1.62, Y_CROSS, "$x$", fontsize=20, color=INK2, va="center", zorder=4)

save(fig, __file__)
