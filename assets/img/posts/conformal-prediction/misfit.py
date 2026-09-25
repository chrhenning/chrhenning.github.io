"""Conformal sets around a model with the wrong mean and one with the wrong spread.

The linear fit is the least-squares optimum, so the misfit comes from the model class, not
from training.

Run: python misfit.py  (requires numpy, matplotlib)
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

ALPHA = 0.1
N_SHOW = 150
rng = np.random.default_rng(2)

SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK2 = "#52514e"
POINT = "#a9a8a3"
SET = "#2a78d6"
SET_PALE = "#cde2fb"
FONT = "Helvetica Neue"


def quantile(scores):
    n = len(scores)
    return np.quantile(scores, np.ceil((n + 1) * (1 - ALPHA)) / n, method="higher")


def make_wrong_mean():
    mu = lambda x: 0.6 * x + 0.8 * np.exp(-(((x - 0.8) / 0.08) ** 2))
    sample = lambda n: (lambda x: (x, mu(x) + 0.08 * rng.standard_normal(n)))(rng.uniform(0, 1, n))
    x, y = sample(200_000)
    slope, intercept = np.polyfit(x, y, 1)
    fit = lambda x: slope * x + intercept
    std = np.std(y - fit(x))  # max-likelihood fixed variance of the linear-Gaussian model
    return dict(
        title="Wrong mean",
        subtitle="a straight line fit to a mean with a bump",
        sample=sample, true_mu=mu, mu=fit, scale=lambda x: np.full_like(x, std),
    )


def make_wrong_spread():
    mu = lambda x: 0.35 * np.sin(2 * np.pi * x)
    sigma = lambda x: 0.03 + 0.12 / (1 + np.exp(-(x - 0.85) / 0.04))
    sample = lambda n: (lambda x: (x, mu(x) + sigma(x) * rng.standard_normal(n)))(
        rng.uniform(0, 1, n))
    return dict(
        title="Wrong spread",
        subtitle="the right mean, but the noise expected on the wrong side",
        sample=sample, true_mu=mu, mu=mu, scale=lambda x: sigma(1 - x),
    )


plt.rcParams.update({"font.family": FONT, "font.size": 10, "axes.edgecolor": INK2,
                     "axes.labelcolor": INK2, "xtick.color": INK, "text.color": INK})
fig, axes = plt.subplots(1, 2, figsize=(12, 4.6), facecolor=SURFACE)
xg = np.linspace(0, 1, 500)

for ax, case in zip(axes, (make_wrong_mean(), make_wrong_spread())):
    mu, scale = case["mu"], case["scale"]
    xc, yc = case["sample"](20_000)
    xt, yt = case["sample"](200_000)
    q = quantile(np.abs(yc - mu(xc)) / scale(xc))
    covered = np.abs(yt - mu(xt)) <= q * scale(xt)

    ax.fill_between(xg, mu(xg) - q * scale(xg), mu(xg) + q * scale(xg), color=SET_PALE, lw=0,
                    zorder=0)
    ax.scatter(xt[:N_SHOW], yt[:N_SHOW], s=22, color=INK2, alpha=0.55, lw=0, zorder=1)
    ax.plot(xg, case["true_mu"](xg), color=POINT, lw=2, zorder=2)
    ax.plot(xg, mu(xg), color=SET, lw=2, zorder=3)
    for sign in (-1, 1):
        ax.plot(xg, mu(xg) + sign * scale(xg), color=SET, lw=1, ls=(0, (3, 2.5)), zorder=3)

    ax.set_xticks([])

    ax.text(0, 1.11, case["title"], transform=ax.transAxes, fontsize=18, fontweight="bold",
            in_layout=False)
    ax.text(0, 1.035, case["subtitle"], transform=ax.transAxes, fontsize=14.5, color=INK2,
            in_layout=False)
    ax.set_facecolor(SURFACE)
    ax.set_xlim(0, 1)
    ax.set_yticks([])
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(POINT)
    print(f"{case['title']}: coverage {covered.mean():.3f}")

handles = [
    Line2D([], [], ls="", marker="o", ms=5, color=INK2, alpha=0.55, label="data"),
    Line2D([], [], color=POINT, lw=2, label="true mean"),
    Line2D([], [], color=SET, lw=2, label="model mean"),
    Line2D([], [], color=SET, lw=1, ls=(0, (3, 2.5)), label="± 1 model std"),
    Patch(color=SET_PALE, label="conformal set, 90% overall"),
]
fig.legend(handles=handles, loc="lower center", ncol=5, frameon=False, fontsize=14,
           bbox_to_anchor=(0.5, 0.005), columnspacing=2.2)
fig.tight_layout(rect=(0, 0.08, 1, 0.88), w_pad=5)
fig.savefig(Path(__file__).with_suffix(".png"), dpi=180, facecolor=SURFACE)
