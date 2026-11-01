"""The three sources of uncertainty in the hypothesis space.

Aleatoric: the spread of the truth itself. Approximation: the posterior's spread within the model.
Model: the gap between the best hypothesis in the model and the truth. A sketch, not computed.

Run: python 16_uncertainty_sources.py  (requires numpy, scipy, matplotlib)
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_rgb
from matplotlib.patches import Polygon
from scipy.stats import norm

from common import (INK2, MODEL, POINT, SPACE, SURFACE, TRUTH, TRUTH_XY, draw_model_blob,
                    draw_truth_star, model_outline, save, setup_style, space_outline,
                    style_space_axes)

POSTERIOR_COV = np.array([[0.02, 0.006], [0.006, 0.015]])

setup_style()
fig, ax = plt.subplots(figsize=(4.8, 5.2), facecolor=SURFACE)
style_space_axes(ax)
ax.set_xlim(-1.15, 2.0)
bx, by = space_outline()
ax.fill(bx, by, color=SPACE, lw=0, zorder=0)
ax.plot(bx, by, color=POINT, lw=1.2, zorder=1)
ax.text(0, 2.05, "all conditional\n" r"distributions $p(y \mid x)$", fontsize=18,
        ha="center", va="bottom", color=INK2)
draw_model_blob(ax, label="")
ax.text(-0.1, -0.95, r"model $\{p_\theta\}$", fontsize=16, color=MODEL, ha="center",
        va="center", zorder=6)
draw_truth_star(ax, label=False)

mx, my = model_outline()
i = np.argmin(np.hypot(mx - TRUTH_XY[0], my - TRUTH_XY[1]))
best = np.array([mx[i], my[i]])
centre = best + 0.12 * (np.array([-0.1, -0.75]) - best)

gx, gy = np.meshgrid(np.linspace(-0.8, 0.6, 300), np.linspace(-1.5, 0.0, 300))
diff = np.stack([gx - centre[0], gy - centre[1]], axis=-1)
dens = np.exp(-0.5 * np.einsum("...i,ij,...j->...", diff, np.linalg.inv(POSTERIOR_COV), diff))
rgba = np.zeros((*gx.shape, 4))
rgba[..., :3] = to_rgb(MODEL)
rgba[..., 3] = 0.8 * dens
shade = ax.imshow(rgba, origin="lower", extent=(-0.8, 0.6, -1.5, 0.0), aspect="auto",
                  interpolation="bilinear", zorder=4)
shade.set_clip_path(Polygon(np.column_stack([mx, my]), transform=ax.transData))
t = np.linspace(0, 2 * np.pi, 200)
(ring,) = ax.plot(*(centre[:, None] + 2 * np.linalg.cholesky(POSTERIOR_COV) @ [np.cos(t), np.sin(t)]),
                  color=MODEL, lw=1.2, zorder=4)
# The posterior lives only on the model.
ring.set_clip_path(Polygon(np.column_stack([mx, my]), transform=ax.transData))
ax.plot(*best, "o", ms=6, color=MODEL, mec="white", mew=1, zorder=5)
ax.plot([best[0], TRUTH_XY[0]], [best[1], TRUTH_XY[1]], color=INK2, lw=1.4, ls=(0, (4, 3)),
        zorder=5)

ys = np.linspace(-1, 1, 200)
curve = 0.5 * norm.pdf(ys, -0.5, 0.15) + 0.5 * norm.pdf(ys, 0.5, 0.15)
ax.fill_between(TRUTH_XY[0] + 0.28 * ys, 0.85, 0.85 + 0.13 * curve, color=TRUTH, alpha=0.35,
                lw=0, zorder=5)
ax.plot(TRUTH_XY[0] + 0.28 * ys, 0.85 + 0.13 * curve, color=TRUTH, lw=1.4, zorder=5)

for (x, y), (tx, ty), text, color in (
        ((0.6, 1.05), (1.15, 1.25), "aleatoric", TRUTH),
        (tuple((best + TRUTH_XY) / 2), (1.15, 0.2), "model", INK2),
        (tuple(centre + [0.12, -0.02]), (1.15, -0.65), "approximation", MODEL)):
    ax.annotate(text, (x, y), (tx, ty), fontsize=16, color=color, va="center",
                arrowprops=dict(arrowstyle="-", color=color, lw=1, shrinkA=2, shrinkB=0),
                zorder=6)

save(fig, __file__)
