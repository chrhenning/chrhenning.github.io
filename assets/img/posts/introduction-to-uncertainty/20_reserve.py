"""The best reserve is a quantile of the predicted shortfall.

Run: python 20_reserve.py  (requires numpy, scipy, matplotlib)
"""

import matplotlib.pyplot as plt
import numpy as np

from common import INK2, MODEL, POINT, SURFACE, save, setup_style
from reserve import model_pdf, model_quantile

TAU = 0.95

ys = np.linspace(-3.5, 5, 600)
py = model_pdf(ys)
r = model_quantile(TAU)

setup_style()
fig, ax = plt.subplots(figsize=(6.4, 3.4), facecolor=SURFACE)
ax.set_facecolor(SURFACE)
ax.fill_between(ys, 0, py, color=MODEL, alpha=0.12, lw=0)
ax.fill_between(ys[ys >= r], 0, py[ys >= r], color=MODEL, alpha=0.6, lw=0)
ax.plot(ys, py, color=MODEL, lw=2.2)
ax.axvline(r, ymax=0.8, color=INK2, lw=2)

ax.text(r, py.max() * 1.1, "reserve", color=INK2, fontsize=17, ha="center", va="bottom")
ax.annotate("shortage\nchance $1 - \\tau$", xy=(r + 0.35, model_pdf(r + 0.35) * 0.4),
            xytext=(r + 1.1, py.max() * 0.45), color=MODEL, fontsize=16, ha="left",
            va="center", arrowprops=dict(arrowstyle="-", color=MODEL, lw=1.2))

ax.set_xlim(ys[0], ys[-1])
ax.set_ylim(0, py.max() * 1.3)
ax.set_xlabel("shortfall", fontsize=17, color=INK2)
ax.set_xticks([])
ax.set_yticks([])
for side in ("top", "right", "left"):
    ax.spines[side].set_visible(False)
ax.spines["bottom"].set_color(POINT)

save(fig, __file__)
