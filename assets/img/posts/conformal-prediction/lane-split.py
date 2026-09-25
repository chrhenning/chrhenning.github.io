"""Conformal sets at the lane split: three likelihoods, and one bimodal model with two scores.

Each model is the analytic optimum of its likelihood, so training can't explain the result.

Run: python lane-split.py  (requires numpy, matplotlib)
"""

from math import erf, sqrt
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

ALPHA = 0.1
FORK = 0.8
X_SLICE = 0.97
SIGMA = 0.25
Y_LIM = 3.0
N_BINS = 40
rng = np.random.default_rng(0)

SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK2 = "#52514e"
TRUE = "#a9a8a3"
SET = "#2a78d6"
SET_PALE = "#cde2fb"
TRUE_FILL = "#e6e5e1"
FONT = "Helvetica Neue"
STRIP_LW = 6


# Most of the road is a single lane, so the fork is rare and the global threshold ignores it.
def m(x):
    t = np.clip((x - FORK) / (1 - FORK), 0, 1)
    return 1.6 * t * t * (3 - 2 * t)


def sample(n):
    x = rng.uniform(0, 1, n)
    sign = rng.choice([-1, 1], n)
    y = sign * m(x) + SIGMA * rng.standard_normal(n)
    return x, y


Phi = np.vectorize(lambda z: 0.5 * (1 + erf(z / sqrt(2))))
edges = np.linspace(-Y_LIM, Y_LIM, N_BINS + 1)
width = edges[1] - edges[0]
centers = 0.5 * (edges[:-1] + edges[1:])


def true_density(x, y):
    n = lambda mu: np.exp(-0.5 * ((y - mu) / SIGMA) ** 2) / (SIGMA * np.sqrt(2 * np.pi))
    return 0.5 * n(m(x)) + 0.5 * n(-m(x))


def bin_probs(x):
    x = np.atleast_1d(x)[:, None]
    cdf = lambda mu: Phi((edges[None, :] - mu) / SIGMA)
    c = 0.5 * cdf(m(x)) + 0.5 * cdf(-m(x))
    p = np.diff(c, axis=1)
    return p / p.sum(axis=1, keepdims=True)


def to_bin(y):
    return np.clip(np.digitize(y, edges) - 1, 0, N_BINS - 1)


def quantile(scores):
    n = len(scores)
    return np.quantile(scores, np.ceil((n + 1) * (1 - ALPHA)) / n, method="higher")


def flow_sd(x):
    return np.sqrt(m(x) ** 2 + SIGMA**2)


xc, yc = sample(20_000)
v_mse = np.mean(yc**2)  # MSE fixes the variance; this is its max-likelihood value around f = 0
q_gauss = quantile(np.abs(yc))
q_flow_mv = quantile(np.abs(yc) / flow_sd(xc))
t_flow = -quantile(-true_density(xc, yc))
t_cls = 1 - quantile(1 - bin_probs(xc)[np.arange(len(xc)), to_bin(yc)])

xt, yt = sample(200_000)
cov = {
    "gauss": np.mean(np.abs(yt) <= q_gauss),
    "cls": np.mean(bin_probs(xt)[np.arange(len(xt)), to_bin(yt)] >= t_cls),
    "flow_mv": np.mean(np.abs(yt) <= q_flow_mv * flow_sd(xt)),
    "flow_dens": np.mean(true_density(xt, yt) >= t_flow),
}
cov["het"] = cov["flow_mv"]

ys = np.linspace(-Y_LIM, Y_LIM, 2001)
dy = ys[1] - ys[0]
gaussian = lambda v: np.exp(-0.5 * ys**2 / v) / np.sqrt(2 * np.pi * v)
p_true = true_density(X_SLICE, ys)
p_gauss = gaussian(v_mse)
# The Gaussian optimum matches the mixture's mean and variance.
p_het = gaussian(flow_sd(X_SLICE) ** 2)
p_bins = bin_probs(X_SLICE)[0]
inside = {
    "gauss": np.abs(ys) <= q_gauss,
    "cls": p_bins >= t_cls,
    "flow_mv": np.abs(ys) <= q_flow_mv * flow_sd(X_SLICE),
    "flow_dens": p_true >= t_flow,
}
inside["het"] = inside["flow_mv"]
cov_slice = {k: np.sum(p_true[v]) * dy for k, v in inside.items() if k != "cls"}
cov_slice["cls"] = np.sum(p_bins[inside["cls"]])
for k in cov:
    print(f"{k:9s} coverage overall {cov[k]:.3f}  at x={X_SLICE}: {cov_slice[k]:.3f}")

plt.rcParams.update({
    "font.family": FONT, "font.size": 10, "mathtext.fontset": "custom",
    "mathtext.rm": FONT, "mathtext.it": f"{FONT}:italic",
    "axes.edgecolor": INK2, "axes.labelcolor": INK2, "xtick.color": INK2, "text.color": INK,
})

def draw(ax, k, name, score, model, thresh):
    truth = p_true * width if model is None else p_true
    top = 1.3 * (truth.max() if model is None else max(truth.max(), model.max()))
    strip_y = -0.07 * top
    ins = inside[k]

    ax.fill_between(ys, truth, color=TRUE_FILL, lw=0, zorder=0)
    if model is None:
        ax.bar(centers, p_bins, width=width * 0.82, color=np.where(ins, SET, SET_PALE), zorder=2)
        on = np.repeat(ins, 2)
        ax.plot(np.where(on, np.repeat(edges, 2)[1:-1], np.nan), np.full(on.size, strip_y),
                color=SET, lw=STRIP_LW, solid_capstyle="butt")
    else:
        ax.fill_between(ys, model, where=ins, color=SET_PALE, lw=0, zorder=1)
        ax.plot(ys, model, color=SET, lw=2, zorder=2)
        ax.plot(np.where(ins, ys, np.nan), np.full_like(ys, strip_y), color=SET,
                lw=STRIP_LW, solid_capstyle="butt")
    if thresh is not None:
        ax.axhline(thresh, color=INK2, lw=1, ls=(0, (4, 3)), zorder=3)
    ax.axvline(0, color=INK2, lw=0.8, ls=(0, (1, 2.5)), zorder=0)

    ax.text(0, 1.13, name, transform=ax.transAxes, fontsize=17, fontweight="bold", in_layout=False)
    ax.text(0, 1.025, f"score  {score}", transform=ax.transAxes, fontsize=14.5, color=INK2,
            in_layout=False)

    ax.set_facecolor(SURFACE)
    ax.set_xlim(-2.8, 2.8)
    ax.set_ylim(2 * strip_y, top)
    ax.set_yticks([])
    ax.set_xlabel("steering angle", fontsize=14)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_position(("data", 2 * strip_y))
    ax.spines["bottom"].set_color(TRUE)
    ax.tick_params(axis="x", length=0, pad=6, labelsize=13)


handles = [
    Patch(color=TRUE_FILL, label="true distribution"),
    Line2D([], [], color=SET, lw=2, label="model"),
    Line2D([], [], color=INK2, lw=1, ls=(0, (4, 3)), label="conformal threshold"),
    Line2D([], [], color=SET, lw=STRIP_LW, label="conformal set"),
]

# No threshold line where the set is not a level set of the model's density.
figures = {
    "lane-split": [
        ("gauss", "Point regressor (MSE)", r"$|y - f(x)|$", p_gauss,
         p_gauss[inside["gauss"]].min()),
        ("het", "Heteroscedastic Gaussian", r"$|y - f(x)|\ /\ \sigma(x)$", p_het,
         p_het[inside["het"]].min()),
        ("cls", "Categorical over buckets", r"$1 - \hat{p}(\mathrm{bucket} \mid x)$", None, t_cls),
    ],
    "lane-split-score": [
        ("flow_mv", "Score from mean and spread", r"$|y - f(x)|\ /\ \sigma(x)$", p_true, None),
        ("flow_dens", "Score from density", r"$-\hat{p}(y \mid x)$", p_true, t_flow),
    ],
}
for stem, panels in figures.items():
    fig, axes = plt.subplots(1, len(panels), figsize=(5.5 * len(panels), 4.4),
                             facecolor=SURFACE)
    for ax, panel in zip(axes, panels):
        draw(ax, *panel)
    axes[0].text(0.06, axes[0].get_ylim()[1] * 0.97, "divider", fontsize=12.5, color=INK2,
                 va="top")
    fig.legend(handles=handles, loc="lower center", ncol=4, frameon=False, fontsize=14,
               bbox_to_anchor=(0.5, 0.005), handlelength=2.2, columnspacing=2)
    fig.tight_layout(rect=(0, 0.1, 1, 0.88), w_pad=4)
    fig.savefig(Path(__file__).with_name(f"{stem}.png"), dpi=180, facecolor=SURFACE)
