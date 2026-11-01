"""With enough data, the mixture model matches the bimodal truth in the middle lane.

The right panel is the slice x = middle of the left panel, turned sideways so the axes line up.

Run: python 12_aleatoric.py  (requires numpy, scipy, matplotlib)
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import ConnectionPatch

from common import (INK2, LANES, MODEL, POINT, SURFACE, TRUTH, Y_LIM, lane_modes, save,
                    setup_style, style_data_axes, true_density)
from mdn import draw_fit, fit, model_density

X_MIDDLE = 0.0
HALF_WIDTH = 0.07

setup_style()
fig = plt.figure(figsize=(11, 5), facecolor=SURFACE)
ax = fig.add_axes((0.08, 0.17, 0.42, 0.7))
style_data_axes(ax)
ax.set_xticks([c for c, _ in LANES], ["left", "middle", "right"], fontsize=14, color=INK2)
ax.tick_params(axis="x", length=3, color=POINT)
ax.set_xlabel("lane position $x$", fontsize=17, color=INK2, labelpad=4)

x, y, params = fit(2000, 0)
draw_fit(ax, params)
ax.scatter(x[:300], y[:300], s=7, color=INK2, alpha=0.5, lw=0, zorder=2)
ax.axvspan(X_MIDDLE - HALF_WIDTH, X_MIDDLE + HALF_WIDTH, fc=TRUTH, alpha=0.15, ec="none",
           zorder=3)
for edge in (X_MIDDLE - HALF_WIDTH, X_MIDDLE + HALF_WIDTH):
    ax.axvline(edge, color=TRUTH, lw=1.2, zorder=3)
ax.text(0, 1.04, "$n = 2{,}000$", transform=ax.transAxes, fontsize=18, color=INK2)

ax_slice = fig.add_axes((0.62, 0.17, 0.3, 0.7), sharey=ax)
ax_slice.set_facecolor(SURFACE)
ys = np.linspace(*Y_LIM, 1000)
truth = true_density(np.full_like(ys, X_MIDDLE), ys)
model = model_density(params, np.full_like(ys, X_MIDDLE), ys)
ax_slice.fill_betweenx(ys, 0, truth, color=TRUTH, alpha=0.35, lw=0)
ax_slice.plot(truth, ys, color=TRUTH, lw=2.2)
ax_slice.plot(model, ys, color=MODEL, lw=2.2, ls=(0, (5, 2.5)))
top = max(truth.max(), model.max())
ax_slice.set_xlim(0, top * 1.9)

left, right = lane_modes(X_MIDDLE)
for mode, text in ((left, "take the\nleft lane"), (right, "take the\nright lane")):
    ax_slice.text(top * 1.12, mode, text, fontsize=16, color=TRUTH, va="center")
ax_slice.text(1, 1.04, r"$p(y \mid x = \mathrm{middle})$", transform=ax_slice.transAxes,
              fontsize=18, color=INK2, ha="right")
ax_slice.set_xticks([])
ax_slice.tick_params(axis="y", left=False, labelleft=False)
for side in ("top", "right", "bottom"):
    ax_slice.spines[side].set_visible(False)
ax_slice.spines["left"].set_color(TRUTH)
ax_slice.spines["left"].set_linewidth(1.2)

fig.add_artist(ConnectionPatch((X_MIDDLE, Y_LIM[1]), (0, Y_LIM[1]), "data", "data",
                               axesA=ax, axesB=ax_slice, color=TRUTH, lw=1.4,
                               arrowstyle="-|>", mutation_scale=16,
                               connectionstyle="arc3,rad=-0.12", zorder=4))

save(fig, __file__)
