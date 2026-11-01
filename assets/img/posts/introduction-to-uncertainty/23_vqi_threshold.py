"""The same conformal guarantee on defects costs few or many false rejects.

Run: python 23_vqi_threshold.py  (requires numpy, scipy, matplotlib)
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

from common import INK2, MODEL, POINT, SURFACE, TRUTH, save, setup_style

ALPHA = 0.05
GOOD_PALE = "#dddcd7"
x = np.linspace(-3.5, 7.5, 600)

setup_style()
fig, axes = plt.subplots(2, 1, figsize=(7, 7.5), facecolor=SURFACE, sharex=True)

for ax, (name, defect_mean) in zip(axes, [("good model", 3.5), ("weak model", 1.5)]):
    ax.set_facecolor(SURFACE)
    good, defect = norm.pdf(x), norm.pdf(x, defect_mean)
    # Threshold at the alpha quantile of the defect scores: at most alpha escape.
    t = defect_mean + norm.ppf(ALPHA)
    false_rejects = norm.sf(t)
    # AUROC of two unit-variance Gaussians.
    auroc = norm.cdf(defect_mean / np.sqrt(2))

    ax.fill_between(x, defect, color=TRUTH, alpha=0.2, lw=0)
    ax.fill_between(x, good, color=GOOD_PALE, alpha=0.7, lw=0)
    ax.fill_between(x, good, where=x >= t, color=INK2, alpha=0.75, lw=0)
    ax.plot(x, good, color=POINT, lw=1.6)
    ax.plot(x, defect, color=TRUTH, lw=2.2)

    top = good.max()
    ax.plot([t, t], [0, top * 1.12], color=MODEL, lw=2.4)
    ax.text(-1.5, top * 0.6, "good\nparts", fontsize=22, color=INK2, ha="right")
    ax.text(defect_mean + 0.9, top * 0.85, "defects", fontsize=22, color=TRUTH, ha="left")
    ax.text(-3.4, top * 1.6, f"{name} (AUROC {auroc:.2f})\n{false_rejects:.0%} false rejects",
            fontsize=22, color=INK2, va="top", linespacing=1.3)

    ax.set_ylim(0, top * 1.62)
    ax.set_yticks([])
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(POINT)

axes[-1].set_xlim(x[0], x[-1])
axes[-1].set_xticks([])
axes[-1].set_xlabel(r"defect score $\rightarrow$", fontsize=22, color=INK2, labelpad=6)
fig.suptitle(f"threshold set so that {ALPHA:.0%} of defects escape", fontsize=22, color=MODEL)
fig.tight_layout(h_pad=2.5)

save(fig, __file__)
