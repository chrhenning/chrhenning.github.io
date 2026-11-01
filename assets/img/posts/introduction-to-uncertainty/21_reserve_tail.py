"""The Gaussian sets the right reserve at 90% but too little at 99%.

Run: python 21_reserve_tail.py  (requires numpy, scipy, matplotlib)
"""

import matplotlib.pyplot as plt
import numpy as np

from common import MODEL, SURFACE, TRUTH, save, setup_style
from reserve import (model_quantile, model_sf, style_exceedance_axes, true_quantile,
                     true_sf)

ys = np.linspace(-1, 7, 600)

setup_style()
fig, ax = plt.subplots(figsize=(6.4, 4.2), facecolor=SURFACE)
style_exceedance_axes(ax, ys)
ax.plot(ys, true_sf(ys), color=TRUTH, lw=2.4, label="truth")
ax.plot(ys, model_sf(ys), color=MODEL, lw=2.4, label="Gaussian")

for tau in (0.9, 0.99):
    rm, rt = model_quantile(tau), true_quantile(tau)
    ax.plot([ys[0], max(rm, rt)], [1 - tau] * 2, color="#a9a8a3", lw=1, ls=(0, (4, 3)),
            zorder=0)
    for r, c in ((rm, MODEL), (rt, TRUTH)):
        ax.plot([r, r], [5e-4, 1 - tau], color=c, lw=1.4, ls=(0, (4, 3)))
        ax.plot(r, 1 - tau, "o", color=c, ms=7, zorder=5)

ax.legend(frameon=False, fontsize=15, loc="upper right")
save(fig, __file__)
