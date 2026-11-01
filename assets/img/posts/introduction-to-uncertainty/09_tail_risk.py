"""A loss distribution whose mean looks harmless but whose tail holds rare, costly outcomes.

Run: python 09_tail_risk.py  (requires numpy, scipy, matplotlib)
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

from common import INK2, MODEL, POINT, SURFACE, TRUTH, save, setup_style

W_TAIL, MU_TAIL, STD_TAIL = 0.05, 4.6, 0.55


def density(x):
    return (1 - W_TAIL) * norm.pdf(x, 0, 1) + W_TAIL * norm.pdf(x, MU_TAIL, STD_TAIL)


xs = np.linspace(-3.5, 7, 800)
px = density(xs)
mean = W_TAIL * MU_TAIL
cdf = np.cumsum(px) * (xs[1] - xs[0])
var95 = xs[np.searchsorted(cdf, 0.95)]

setup_style()
fig, ax = plt.subplots(figsize=(6.4, 3.2), facecolor=SURFACE)
ax.set_facecolor(SURFACE)
ax.fill_between(xs, 0, px, color=INK2, alpha=0.12, lw=0)
tail = xs >= var95
ax.fill_between(xs[tail], 0, px[tail], color=TRUTH, alpha=0.6, lw=0)
ax.plot(xs, px, color=INK2, lw=2)
ax.plot(xs, norm.pdf(xs, mean, 1), color=POINT, lw=1.6, ls=(0, (4, 3)))
ax.axvline(mean, ymax=0.84, color=MODEL, lw=2.2)

ax.text(mean, px.max() * 1.12, "mean", color=MODEL, fontsize=17, ha="center", va="bottom")
ax.text(MU_TAIL, density(MU_TAIL) + 0.05, "tail risk", color=TRUTH, fontsize=17,
        ha="center", va="bottom")

ax.set_xlim(xs[0], xs[-1])
ax.set_ylim(0, px.max() * 1.3)
ax.set_xlabel("loss", fontsize=17, color=INK2)
ax.set_xticks([])
ax.set_yticks([])
for side in ("top", "right", "left"):
    ax.spines[side].set_visible(False)
ax.spines["bottom"].set_color(POINT)

save(fig, __file__)
