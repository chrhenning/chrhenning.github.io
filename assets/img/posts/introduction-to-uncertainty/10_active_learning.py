"""Active learning: query the label where the model is least certain.

Run: python 10_active_learning.py  (requires numpy, scipy, matplotlib)
"""

import matplotlib.pyplot as plt
import numpy as np

from common import INK2, MODEL, POINT, SURFACE, TRUTH, save, setup_style

LENGTH, SIGNAL, NOISE = 0.8, 1.0, 0.1


def kernel(a, b):
    return SIGNAL**2 * np.exp(-0.5 * (a[:, None] - b[None, :]) ** 2 / LENGTH**2)


def truth(x):
    return np.sin(1.3 * x) + 0.3 * x


rng = np.random.default_rng(4)
x_train = np.concatenate([rng.uniform(-4.5, -1.2, 7), rng.uniform(2.2, 4.5, 5)])
y_train = truth(x_train) + NOISE * rng.standard_normal(len(x_train))

xs = np.linspace(-4.5, 4.5, 400)
K = kernel(x_train, x_train) + NOISE**2 * np.eye(len(x_train))
K_s = kernel(xs, x_train)
mean = K_s @ np.linalg.solve(K, y_train)
std = np.sqrt(SIGNAL**2 - np.sum(K_s * np.linalg.solve(K, K_s.T).T, axis=1) + NOISE**2)
x_next = xs[np.argmax(std)]

setup_style()
fig, ax = plt.subplots(figsize=(6.4, 4.8), facecolor=SURFACE)
ax.set_facecolor(SURFACE)
ax.fill_between(xs, mean - 2 * std, mean + 2 * std, color=MODEL, alpha=0.2, lw=0)
ax.plot(xs, mean, color=MODEL, lw=2.2)
ax.scatter(x_train, y_train, s=36, color=INK2, lw=0, zorder=3)

ax.axvline(x_next, ymax=0.86, color=TRUTH, lw=2, ls=(0, (4, 3)))
ax.text(x_next, 3.2, "next query", color=TRUTH, fontsize=17, ha="center", va="center")

ax.set_xlim(xs[0], xs[-1])
ax.set_ylim(-3.6, 3.6)
ax.set_xlabel("input $x$", fontsize=17, color=INK2)
ax.set_ylabel("output $y$", fontsize=17, color=INK2)
ax.set_xticks([])
ax.set_yticks([])
for side in ("top", "right"):
    ax.spines[side].set_visible(False)
for side in ("left", "bottom"):
    ax.spines[side].set_color(POINT)

save(fig, __file__)
