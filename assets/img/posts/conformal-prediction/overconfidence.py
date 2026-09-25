"""Conformal sets for two classifiers with the same predictions and the same confidences.

The right one assigns the confidences to random inputs, so it is equally sure when wrong.

Run: python overconfidence.py  (requires numpy, matplotlib)
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

ALPHA = 0.1
K = 5
rng = np.random.default_rng(3)

SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK2 = "#52514e"
POINT = "#a9a8a3"
SET = "#2a78d6"
FONT = "Helvetica Neue"


def quantile(scores):
    n = len(scores)
    return np.quantile(scores, np.ceil((n + 1) * (1 - ALPHA)) / n, method="higher")


def sample(n):
    logits = rng.uniform(0.5, 5, n)[:, None] * rng.standard_normal((n, K))
    p = np.exp(logits - logits.max(axis=1, keepdims=True))
    p /= p.sum(axis=1, keepdims=True)
    y = (rng.random(n)[:, None] > np.cumsum(p, axis=1)).sum(axis=1)
    return p, y


def shuffle(p):
    # Confidence borrowed from a random other input says nothing about this one.
    profiles = -np.sort(-p, axis=1)[rng.permutation(len(p))]
    out = np.empty_like(p)
    np.put_along_axis(out, np.argsort(-p, axis=1), profiles, axis=1)
    return out


plt.rcParams.update({"font.family": FONT, "font.size": 10, "axes.edgecolor": INK2,
                     "axes.labelcolor": INK2, "xtick.color": INK, "text.color": INK})
fig, axes = plt.subplots(1, 2, figsize=(10, 4.2), facecolor=SURFACE, sharey=True)

pc, yc = sample(20_000)
pt, yt = sample(200_000)
sizes = np.arange(K + 1)
width = 0.38

cases = [("Less sure when wrong", lambda p: p),
         ("Equally sure when wrong", shuffle)]
for ax, (title, model) in zip(axes, cases):
    phat_c, phat_t = model(pc), model(pt)
    q = quantile(1 - phat_c[np.arange(len(yc)), yc])
    sets = phat_t >= 1 - q
    size = sets.sum(axis=1)
    right = phat_t.argmax(axis=1) == yt
    coverage = sets[np.arange(len(yt)), yt].mean()

    for offset, mask, color in ((-width / 2, right, SET), (width / 2, ~right, POINT)):
        share = np.bincount(size[mask], minlength=K + 1) / mask.sum()
        ax.bar(sizes + offset, share, width, color=color, lw=0)

    ax.text(0, 1.06, title, transform=ax.transAxes, fontsize=18, fontweight="bold",
            in_layout=False)
    ax.text(0.03, 0.95, f"average set size: {size[right].mean():.1f} right, "
            f"{size[~right].mean():.1f} wrong", transform=ax.transAxes, fontsize=13.5,
            color=INK2, va="top", in_layout=False)
    ax.set_xticks(sizes[1:])
    ax.tick_params(axis="x", labelsize=14)
    ax.set_xlim(0.4, K + 0.6)
    ax.set_ylim(0, 0.9)
    ax.set_xlabel("set size", fontsize=14)
    ax.set_facecolor(SURFACE)
    ax.set_yticks([])
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(POINT)
    print(f"{title}: accuracy {right.mean():.3f}, coverage {coverage:.3f}")

handles = [Patch(color=SET, label="model right"), Patch(color=POINT, label="model wrong")]
fig.legend(handles=handles, loc="lower center", ncol=2, frameon=False, fontsize=14,
           bbox_to_anchor=(0.5, 0.005), columnspacing=2.2)
fig.tight_layout(rect=(0, 0.08, 1, 0.92), w_pad=4)
fig.savefig(Path(__file__).with_suffix(".png"), dpi=180, facecolor=SURFACE)
