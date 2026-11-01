"""The conformal threshold is the 90% quantile of the scores on the calibration set.

Run: python 18_conformal_recipe.py  (requires numpy, scipy, matplotlib)
"""

import matplotlib.pyplot as plt
import numpy as np

from common import INK2, MODEL, MODEL_PALE, POINT, SURFACE, save, setup_style
from conformal import calibrate

_, _, _, scores, q = calibrate()
s, q = scores["mse"], q["mse"]

setup_style()
fig, ax = plt.subplots(figsize=(8, 5), facecolor=SURFACE)
ax.set_facecolor(SURFACE)

bins = np.linspace(0, s.max() * 1.02, 40)
counts, edges, patches = ax.hist(s, bins=bins, color=MODEL_PALE, ec=SURFACE, lw=0.8)
for patch, lo in zip(patches, edges[:-1]):
    if lo >= q:
        patch.set_facecolor(POINT)
top = counts.max()
ax.plot([q, q], [0, top * 1.04], color=MODEL, lw=2.4)
ax.text(q, top * 1.08, r"$\hat q$", fontsize=26, color=MODEL, ha="center", va="bottom")
ax.text(q * 0.5, top * 0.78, "90% of\nscores", fontsize=19, color=MODEL, ha="center")
ax.text((q + bins[-1]) / 2, top * 0.32, "10%", fontsize=19, color=INK2, ha="center")

ax.set_xlim(0, bins[-1])
ax.set_ylim(0, top * 1.25)
ax.set_yticks([])
ax.set_ylabel("count", fontsize=17, color=INK2, labelpad=6)
ax.set_xticks([0], ["0"], fontsize=15, color=INK2)
ax.tick_params(axis="x", length=3, color=POINT)
ax.set_xlabel(r"score $s(x, y) = |y - f(x)|$", fontsize=17,
              color=INK2, labelpad=6)
for side in ("top", "right", "left"):
    ax.spines[side].set_visible(False)
ax.spines["bottom"].set_color(POINT)
ax.text(0, 1.04, "histogram of calibration scores", transform=ax.transAxes, fontsize=18,
        color=INK2)

save(fig, __file__)
