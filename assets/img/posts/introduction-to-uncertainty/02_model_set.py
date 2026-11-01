"""A model is a set of hypotheses indexed by theta; training starts at some theta_0.

Run: python 02_model_set.py  (requires numpy, scipy, matplotlib)
"""

import numpy as np

from common import (INK2, MODEL, draw_linear_hypothesis, draw_model_blob, draw_truth_star,
                    make_layout, sample_truth, save)

rng = np.random.default_rng(0)

INIT_THETA = (0.15, 0.25)
INIT_XY = (-0.3, -0.45)

fig, ax_space, ax_data, ax_px = make_layout()

draw_model_blob(ax_space)
draw_truth_star(ax_space)
ax_space.plot(*INIT_XY, "o", ms=10, color=MODEL, mec="white", mew=1.2, zorder=6)
ax_space.text(INIT_XY[0] + 0.1, INIT_XY[1], r"$p_{\theta_0}$", fontsize=20, color=MODEL,
              ha="left", va="center", zorder=6)

draw_linear_hypothesis(ax_data, INIT_THETA)
xs, ys = sample_truth(120, rng)
ax_data.scatter(xs, ys, s=16, color=INK2, alpha=0.8, lw=0, zorder=2)
ax_data.text(0, 1.04, r"model $p_{\theta_0}(y \mid x)$", transform=ax_data.transAxes,
             fontsize=18, color=MODEL)

save(fig, __file__)
