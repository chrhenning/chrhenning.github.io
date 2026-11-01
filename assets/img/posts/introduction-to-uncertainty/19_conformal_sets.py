"""Three conformal sets, all with 90% coverage, from two models and two scores.

Left: the fixed-variance Gaussian with |y - f(x)|. Middle and right: the same mixture fit,
once with a score from its CDF (a central interval), once with a score from its density.
Shading is the model's predictive density, the outline its conformal set.

Run: python 19_conformal_sets.py  (requires numpy, scipy, matplotlib)
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_rgb
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from scipy.stats import norm

from common import (INK, INK2, LANES, MODEL, MODEL_PALE, POINT, SURFACE,
                    draw_density, sample_truth, save, setup_style)
from conformal import calibrate, mixture_cdf, mse_fit
from mdn import model_density

params, xc, yc, _, q = calibrate()
x_pts, y_pts = sample_truth(300, np.random.default_rng(2))
# Beyond the outer lanes, the minority lane falls below 5% and the central interval jumps
# from one lane to the other, which distracts from the point of the figure.
XLIM = (-0.75, 0.75)
xs = np.linspace(*XLIM, 300)
sigma = np.sqrt(np.mean((yc - mse_fit(xc)) ** 2))
# Taller than Y_LIM, so the fixed-variance band is not cut off.
YLIM = (-1.1, 1.1)
EXTENT = (*XLIM, *YLIM)


def gaussian_density(x, y):
    return norm.pdf(y, mse_fit(x), sigma)


def mixture_density(x, y):
    return model_density(params, x.ravel(), y.ravel()).reshape(x.shape)


def central_interval():
    ys = np.linspace(-1.5, 1.5, 3001)
    X, Y = np.meshgrid(xs, ys)
    inside = np.abs(mixture_cdf(params, X.ravel(), Y.ravel()) - 0.5).reshape(X.shape) <= q["cdf"]
    return (np.array([ys[c].min() for c in inside.T]),
            np.array([ys[c].max() for c in inside.T]))


PANELS = (("Gaussian, fixed variance", r"score $|y - f(x)|$", gaussian_density,
           "same width everywhere"),
          ("Mixture of two Gaussians", r"score $|\hat F(y \mid x) - 1/2|$", mixture_density,
           "the model's central 90%"),
          ("Same mixture", r"score $-\hat p(y \mid x)$", mixture_density,
           "where the model's density is high"))

setup_style()
fig, axes = plt.subplots(1, 3, figsize=(21, 4.4), facecolor=SURFACE, sharey=True)
fig.subplots_adjust(wspace=0.16)

for i, (ax, (model, score, density, caption)) in enumerate(zip(axes, PANELS)):
    ax.set_facecolor(SURFACE)
    draw_density(ax, density, MODEL, extent=EXTENT, alpha=0.45)
    if i == 2:
        ys = np.linspace(*YLIM, 400)
        X, Y = np.meshgrid(xs, ys)
        ax.contour(X, Y, mixture_density(X, Y), levels=[-q["density"]], colors=[MODEL],
                   linewidths=2.4, zorder=3)
        ax.contourf(X, Y, mixture_density(X, Y), levels=[-q["density"], np.inf],
                    colors=[MODEL], alpha=0.12, zorder=1)
    else:
        lo, hi = ((mse_fit(xs) - q["mse"], mse_fit(xs) + q["mse"]) if i == 0
                  else central_interval())
        for edge in (lo, hi):
            ax.plot(xs, edge, color=MODEL, lw=2.4, zorder=3)
        ax.fill_between(xs, lo, hi, color=MODEL, alpha=0.12, lw=0, zorder=1)
    if i == 0:
        # A steep band looks thinner than it is, so show the width at two places.
        for xa in (-0.5, 0.45):
            ax.annotate("", xy=(xa, mse_fit(xa) + q["mse"]), xytext=(xa, mse_fit(xa) - q["mse"]),
                        arrowprops=dict(arrowstyle="<->", color=INK, lw=1.4,
                                        shrinkA=0, shrinkB=0), zorder=4)
    ax.scatter(x_pts, y_pts, s=8, color=INK2, alpha=0.5, lw=0, zorder=2)
    ax.plot(0, 0, marker="X", ms=13, color=INK, mec=SURFACE, mew=1, zorder=4)

    ax.text(0, 1.13, model, transform=ax.transAxes, fontsize=21, color=INK2)
    ax.text(0, 1.03, score, transform=ax.transAxes, fontsize=19, color=INK2)
    ax.text(0.5, -0.27, "set: " + caption, transform=ax.transAxes, fontsize=19, color=MODEL,
            ha="center", va="top")
    ax.set_xlim(*XLIM)
    ax.set_ylim(*YLIM)
    ax.set_xticks([c for c, _ in LANES], ["left", "middle", "right"], fontsize=15, color=INK2)
    ax.tick_params(axis="x", length=3, color=POINT)
    ax.tick_params(axis="y", length=0, pad=6)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(POINT)
    ax.set_xlabel("lane position $x$", fontsize=17, color=INK2, labelpad=4)

axes[0].set_yticks([-0.45, 0.45], ["left", "right"], fontsize=15, color=INK2)
axes[0].annotate("divider", xy=(0.03, -0.02), xytext=(0.12, -0.17), fontsize=16, color=INK,
                 arrowprops=dict(arrowstyle="-", color=INK, lw=1))
axes[0].set_ylabel("steering angle $y$", fontsize=17, color=INK2, labelpad=2)

fig.legend(handles=[Patch(color=MODEL_PALE, label=r"model $\hat p(y \mid x)$"),
                    Patch(fc=(*to_rgb(MODEL), 0.12), ec=MODEL, lw=2.4, label="90% conformal set"),
                    Line2D([], [], marker="o", ls="", color=INK2, alpha=0.6, label="drivers")],
           loc="lower center", bbox_to_anchor=(0.5, -0.33), ncol=3, frameon=False, fontsize=18)

save(fig, __file__)
