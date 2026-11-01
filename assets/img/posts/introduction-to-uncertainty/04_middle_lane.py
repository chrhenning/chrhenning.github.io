"""In the middle lane, the truth is bimodal but the MSE fit steers straight ahead.

The MSE optimum is the conditional mean E[y | x], which sits between the two lanes.

Run: python 04_middle_lane.py  (requires numpy, scipy, matplotlib)
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

from common import (INK2, MODEL, MODEL_STD, POINT, SURFACE, TRUE_STD, TRUTH, Y_LIM, lane_modes,
                    p_right, save, setup_style, true_density)

X_MIDDLE = 0.0

setup_style()
fig, ax = plt.subplots(figsize=(8, 5), facecolor=SURFACE)
ax.set_facecolor(SURFACE)

ys = np.linspace(*Y_LIM, 1000)
truth = true_density(np.full_like(ys, X_MIDDLE), ys)
left, right = lane_modes(X_MIDDLE)
w = p_right(X_MIDDLE)
best_mean = (1 - w) * left + w * right
model = norm.pdf(ys, best_mean, MODEL_STD)

ax.fill_between(ys, 0, truth, color=TRUTH, alpha=0.35, lw=0)
ax.plot(ys, truth, color=TRUTH, lw=2.2)
ax.fill_between(ys, 0, model, color=MODEL, alpha=0.25, lw=0)
ax.plot(ys, model, color=MODEL, lw=2.2)

peak = norm.pdf(0, 0, TRUE_STD) * 0.5
ax.text(left, peak * 1.06, "take the\nleft lane", ha="center", va="bottom", fontsize=17,
        color=TRUTH)
ax.text(right, peak * 1.06, "take the\nright lane", ha="center", va="bottom", fontsize=17,
        color=TRUTH)
ax.annotate("best MSE fit:\ninto the divider", xy=(best_mean + 0.05, model.max() * 0.75),
            xytext=(0.3, model.max() * 0.85), fontsize=17, color=MODEL, va="center",
            arrowprops=dict(arrowstyle="-", color=MODEL, lw=1.2))

ax.text(0, 1.04, r"middle lane:  $p(y \mid x = \mathrm{middle})$", transform=ax.transAxes,
        fontsize=18, color=INK2)
ax.set_xlim(*Y_LIM)
ax.set_ylim(0, model.max() * 1.12)
ax.set_yticks([])
ax.set_xticks([left, 0, right], ["left", "straight", "right"], fontsize=15, color=INK2)
ax.tick_params(axis="x", length=3, color=POINT)
ax.set_xlabel("steering angle $y$", fontsize=17, color=INK2, labelpad=6)
for side in ("top", "right", "left"):
    ax.spines[side].set_visible(False)
ax.spines["bottom"].set_color(POINT)

save(fig, __file__)
