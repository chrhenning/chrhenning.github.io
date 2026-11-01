"""A GP with known, input-dependent noise: aleatoric where the data is noisy, epistemic where
there is no data.

Run: python 08_two_uncertainties.py  (requires numpy, scipy, matplotlib)
"""

import matplotlib.pyplot as plt
import numpy as np

from common import INK2, MODEL, POINT, SURFACE, save, setup_style

LENGTH, SIGNAL = 0.9, 1.0


def kernel(a, b):
    return SIGNAL**2 * np.exp(-0.5 * (a[:, None] - b[None, :]) ** 2 / LENGTH**2)


def truth(x):
    return np.sin(1.3 * x) + 0.3 * x


def noise_std(x):
    return 0.08 + 0.5 * np.exp(-(((x + 2.6) / 1.0) ** 2))


rng = np.random.default_rng(3)
x_train = np.concatenate([rng.uniform(-5.0, -0.8, 45), rng.uniform(2.8, 4.5, 10)])
y_train = truth(x_train) + noise_std(x_train) * rng.standard_normal(len(x_train))

xs = np.linspace(-5.5, 5.5, 400)
K = kernel(x_train, x_train) + np.diag(noise_std(x_train) ** 2)
K_s = kernel(xs, x_train)
mean = K_s @ np.linalg.solve(K, y_train)
epistemic = SIGNAL**2 - np.sum(K_s * np.linalg.solve(K, K_s.T).T, axis=1)
total = np.sqrt(epistemic + noise_std(xs) ** 2)

setup_style()
fig, ax = plt.subplots(figsize=(6.4, 4.8), facecolor=SURFACE)
ax.set_facecolor(SURFACE)
ax.fill_between(xs, mean - 2 * total, mean + 2 * total, color=MODEL, alpha=0.2, lw=0)
ax.plot(xs, mean, color=MODEL, lw=2.2)
ax.scatter(x_train, y_train, s=28, color=INK2, lw=0, zorder=3)

arrow = dict(arrowstyle="-|>", color=INK2, lw=1.2, shrinkA=4, shrinkB=2)
ax.annotate("aleatoric", xy=(-2.6, truth(-2.6) + 1.2), xytext=(-2.6, 3.1), fontsize=17,
            color=INK2, ha="center", arrowprops=arrow)
ax.annotate("epistemic", xy=(1.0, 2.0), xytext=(1.0, 3.1), fontsize=17, color=INK2,
            ha="center", arrowprops=arrow)

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
