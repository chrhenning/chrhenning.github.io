"""The space of all conditional distributions, with the ground truth as one point in it.

Run: python 01_space_and_truth.py  (requires numpy, scipy, matplotlib)
"""

import numpy as np
from scipy.stats import norm

from common import (INK2, POINT, TRUTH, TRUTH_XY, draw_density, draw_truth_star, link,
                    make_layout, sample_truth, save, true_density)

rng = np.random.default_rng(0)

# A few other members of the space, drawn as thumbnails so each point reads as a whole p(y|x).
OTHERS = [
    ((-0.4, 0.68), lambda x, y: norm.pdf(y, 0.4 * x, 0.07)),
    ((-0.5, -0.62), lambda x, y: norm.pdf(y, 0.3 * np.cos(2 * x), 0.05 + 0.12 * (x + 1.6))),
    ((0.4, -1.36), lambda x, y: norm.pdf(y, 0.1, 0.3)),
]

fig, ax_space, ax_data, ax_px = make_layout()

for (px, py), dens in OTHERS:
    ax_space.plot(px, py, "o", ms=6, color=INK2, zorder=3)
    w, h = 0.2, 0.11
    fx, fy = ax_space.transLimits.transform((px, py))
    inset = ax_space.inset_axes((fx - w / 2, fy + 0.03, w, h))
    draw_density(inset, dens, INK2, alpha=0.8)
    inset.set_xticks([])
    inset.set_yticks([])
    for spine in inset.spines.values():
        spine.set_color(POINT)

draw_truth_star(ax_space)

draw_density(ax_data, true_density, TRUTH)
xs, ys = sample_truth(120, rng)
ax_data.scatter(xs, ys, s=16, color=INK2, alpha=0.8, lw=0, zorder=2)
ax_data.text(0, 1.04, r"ground truth $p^*(y \mid x)$", transform=ax_data.transAxes,
             fontsize=18, color=INK2)

link(fig, ax_space, (TRUTH_XY[0] + 0.1, TRUTH_XY[1] + 0.05), ax_data, TRUTH)
save(fig, __file__)
