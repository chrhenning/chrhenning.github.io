"""A mixture density network contains the truth, but needs enough data to find it.

Run: python 06_more_data.py  (requires numpy, scipy, matplotlib)
"""

import matplotlib.pyplot as plt
import numpy as np

from common import (INK2, LANES, MODEL, MODEL_PALE, POINT, ROAD, SPACE, SURFACE, TRUTH_XY,
                    draw_truth_star, input_density, save, setup_style, space_outline,
                    style_data_axes, style_space_axes, true_density)
from mdn import draw_fit, fit, model_density

xg = np.linspace(*ROAD, 201)[1:-1]
px = input_density(xg)
px /= px.sum()
yg = np.linspace(-1.2, 1.2, 1201)


def expected_kl(params):
    X, Y = np.meshgrid(xg, yg, indexing="ij")
    P = true_density(X, Y)
    Q = model_density(params, X.ravel(), Y.ravel()).reshape(X.shape)
    kl = np.sum(P * (np.log(np.maximum(P, 1e-300)) - np.log(np.maximum(Q, 1e-300))), axis=1)
    return np.sum(px * kl * (yg[1] - yg[0]))


def mixture_outline(n=300):
    """A larger blob that contains the truth."""
    t = np.linspace(0, 2 * np.pi, n)
    r = 1 + 0.07 * np.sin(2 * t + 0.6) + 0.05 * np.cos(3 * t + 0.9)
    return 0.0 + 0.82 * r * np.cos(t), -0.15 + 1.45 * r * np.sin(t)


setup_style()
fig = plt.figure(figsize=(11.5, 5.2), facecolor=SURFACE)
ax_space = fig.add_axes((0.0, 0.04, 0.24, 0.84))
style_space_axes(ax_space)
bx, by = space_outline()
ax_space.fill(bx, by, color=SPACE, lw=0, zorder=0)
ax_space.plot(bx, by, color=POINT, lw=1.2, zorder=1)
mx, my = mixture_outline()
ax_space.fill(mx, my, color=MODEL_PALE, alpha=0.8, lw=0, zorder=2)
ax_space.plot(mx, my, color=MODEL, lw=1.6, zorder=3)
ax_space.text(0.0, -1.05, r"model $\{p_\theta\}$", fontsize=16, color=MODEL, ha="center",
              zorder=6)
draw_truth_star(ax_space, label=False)
ax_space.text(0.15, TRUTH_XY[1] + 0.22, r"$p^*(y \mid x)$", fontsize=17, ha="center",
              va="bottom", zorder=6)

fits = [(20, 3), (2000, 0)]
dots = [(-0.05, -0.55), (0.15, 0.28)]
for i, ((n, seed), xy) in enumerate(zip(fits, dots)):
    x, y, params = fit(n, seed)
    kl = expected_kl(params)
    print(f"n={n}: KL {kl:.2f}")

    ax = fig.add_axes((0.31 + i * 0.355, 0.2, 0.3, 0.66))
    style_data_axes(ax)
    if i:
        ax.set_ylabel("")
        ax.set_yticks([])
    ax.set_xticks([c for c, _ in LANES], ["left", "middle", "right"], fontsize=14, color=INK2)
    ax.tick_params(axis="x", length=3, color=POINT)
    ax.set_xlabel("lane position $x$", fontsize=17, color=INK2, labelpad=4)
    draw_fit(ax, params)
    show = slice(0, 300)
    ax.scatter(x[show], y[show], s=16 if n < 100 else 7, color=INK2,
               alpha=0.85 if n < 100 else 0.5, lw=0, zorder=2)
    ax.text(0, 1.04, f"$n = {n:,}$".replace(",", "{,}"), transform=ax.transAxes, fontsize=18,
            color=INK2)
    ax.text(1, 1.04, f"KL = {kl:.2f}", transform=ax.transAxes, fontsize=16, color=INK2,
            ha="right")

    ax_space.plot(*xy, "o", ms=10, color=MODEL, mec="white", mew=1.2, zorder=7)
    ax_space.plot([xy[0], TRUTH_XY[0]], [xy[1], TRUTH_XY[1]], color=INK2, lw=1.2,
                  ls=(0, (3, 2.5)), zorder=5)
    ax_space.text(xy[0] - 0.07, xy[1], f"$n = {n:,}$".replace(",", "{,}"), fontsize=13,
                  color=MODEL, ha="right", va="center", zorder=7)

ax_space.text(0, 2.05, "all conditional\n" r"distributions $p(y \mid x)$", fontsize=18,
              ha="center", va="bottom", color=INK2)
save(fig, __file__)
