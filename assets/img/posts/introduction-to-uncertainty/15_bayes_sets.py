"""Inside the model, the prior softly weights hypotheses; the posterior narrows it down.

A sketch, not computed: the shading is two hand-placed Gaussians.

Run: python 15_bayes_sets.py  (requires numpy, matplotlib)
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_rgb
from matplotlib.patches import Polygon

from common import (INK2, MODEL, POINT, SPACE, SURFACE, TRUTH_XY, draw_truth_star, save,
                    setup_style, space_outline, style_space_axes)

PRIOR = ((0.0, -0.05), np.array([[0.075, 0.015], [0.015, 0.2]]))
POSTERIOR = ((0.17, 0.4), np.array([[0.012, 0.006], [0.006, 0.018]]))


def mixture_outline(n=300):
    t = np.linspace(0, 2 * np.pi, n)
    r = 1 + 0.07 * np.sin(2 * t + 0.6) + 0.05 * np.cos(3 * t + 0.9)
    return 0.0 + 0.82 * r * np.cos(t), -0.15 + 1.45 * r * np.sin(t)


def gaussian(gx, gy, mean, cov):
    diff = np.stack([gx - mean[0], gy - mean[1]], axis=-1)
    return np.exp(-0.5 * np.einsum("...i,ij,...j->...", diff, np.linalg.inv(cov), diff))


def contour(mean, cov, level=2.0, n=200):
    t = np.linspace(0, 2 * np.pi, n)
    pts = level * np.linalg.cholesky(cov) @ np.stack([np.cos(t), np.sin(t)])
    return mean[0] + pts[0], mean[1] + pts[1]


setup_style()
fig, ax = plt.subplots(figsize=(4.6, 5.2), facecolor=SURFACE)
style_space_axes(ax)
ax.set_xlim(-1.15, 1.9)
bx, by = space_outline()
ax.fill(bx, by, color=SPACE, lw=0, zorder=0)
ax.plot(bx, by, color=POINT, lw=1.2, zorder=1)
mx, my = mixture_outline()
ax.plot(mx, my, color=MODEL, lw=1.6, zorder=4)
ax.text(-0.1, -1.24, r"model $\{p_\theta\}$", fontsize=16, color=MODEL, ha="center", zorder=6)
ax.text(0, 2.05, "all conditional\n" r"distributions $p(y \mid x)$", fontsize=18,
        ha="center", va="bottom", color=INK2)
draw_truth_star(ax, label=False)

gx, gy = np.meshgrid(np.linspace(-1, 1, 300), np.linspace(-1.75, 1.45, 450))
rgba = np.zeros((*gx.shape, 4))
rgba[..., :3] = to_rgb(MODEL)
rgba[..., 3] = np.maximum(0.3 * gaussian(gx, gy, *PRIOR), 0.75 * gaussian(gx, gy, *POSTERIOR))
shade = ax.imshow(rgba, origin="lower", extent=(-1, 1, -1.75, 1.45), aspect="auto",
                  interpolation="bilinear", zorder=2)
shade.set_clip_path(Polygon(np.column_stack([mx, my]), transform=ax.transData))
ax.plot(*contour(*PRIOR), color=MODEL, lw=1.2, ls=(0, (4, 3)), zorder=3)
ax.plot(*contour(*POSTERIOR), color=MODEL, lw=1.4, zorder=3)

for (x, y), (tx, ty), text in (((0.5, -0.55), (1.15, -0.9), "prior\n" r"$p(\theta)$"),
                               ((0.37, 0.35), (1.15, 0.2), "posterior\n"
                                r"$p(\theta \mid \mathcal{D})$")):
    ax.annotate(text, (x, y), (tx, ty), fontsize=16, color=MODEL, va="center",
                arrowprops=dict(arrowstyle="-", color=MODEL, lw=1, shrinkA=2, shrinkB=0),
                zorder=6)

save(fig, __file__)
