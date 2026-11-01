"""A year of data pins down the bulk but not the tail.

Run: python 22_tail_data.py  (requires numpy, scipy, matplotlib)
"""

import matplotlib.pyplot as plt
import numpy as np

from common import INK2, MODEL, POINT, SURFACE, TRUTH, save, setup_style
from reserve import model_sf, sample_truth, style_exceedance_axes, true_sf

N_DAYS = 365

ys = np.linspace(-1, 7, 600)
data = np.sort(sample_truth(N_DAYS, np.random.default_rng(3)))
emp = 1 - np.arange(1, N_DAYS + 1) / N_DAYS

setup_style()
fig, ax = plt.subplots(figsize=(6.4, 4.2), facecolor=SURFACE)
style_exceedance_axes(ax, ys)
ax.axhspan(5e-4, 1 / N_DAYS, color="#f1f0ec", lw=0, zorder=0)
ax.text(ys[0] + 0.2, 1.4e-3, "rarer than once a year:\nno data", fontsize=15, color=INK2,
        va="center")
ax.plot(ys, true_sf(ys), color=TRUTH, lw=2.4, label="truth")
ax.plot(ys, model_sf(ys), color=MODEL, lw=2.4, label="Gaussian")
ax.step(data[:-1], emp[:-1], where="post", color=POINT, lw=1.8, label="one year of data")

ax.legend(frameon=False, fontsize=15, loc="upper right")
save(fig, __file__)
