"""The same data, a misspecified and a well-specified model.

Top: one Gaussian whose mean has a Gaussian-process prior. Bottom: the mixture from figure 14.
The mixture weight is fixed to the true one and the noise levels do not depend on x, which keeps
the evidence exact. Each point is assigned to a mode by the sign of y, so the mixture's evidence
is that of the completed data, a lower bound. The space panels are sketches.

Run: python 17_two_models.py  (requires numpy, scipy, matplotlib)
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_rgb
from matplotlib.patches import Polygon
from scipy.special import logsumexp

from common import (INK2, LANES, MODEL, POINT, SPACE, SURFACE, TRUTH, TRUTH_XY, X_LIM,
                    draw_truth_star, model_outline, p_right, sample_inputs, sample_truth, save, setup_style,
                    space_outline, style_data_axes, style_space_axes)

N_DATA = 400
PRIOR_STD, LENGTH = 0.35, 0.3
SIGMAS = np.geomspace(0.04, 0.8, 80)
COLORS = ["#2a78d6", "#8b5cc9", "#17a07b", "#d6457f"]
GAP = (0.12, 0.85)

rng = np.random.default_rng(4)
# The data happen to miss most of the right lane.
x_obs = sample_inputs(2 * N_DATA, rng)
x_obs = x_obs[(x_obs < GAP[0]) | (x_obs > GAP[1])][:N_DATA]
x_obs, y_obs = sample_truth(N_DATA, rng, x_obs)
xs = np.linspace(*X_LIM, 160)
z = rng.standard_normal((len(COLORS), 2, len(xs)))
u = rng.uniform(0.05, 0.95, (len(COLORS), 2))


def kernel(a, b):
    return PRIOR_STD**2 * np.exp(-0.5 * ((a[:, None] - b[None, :]) / LENGTH) ** 2)


def gp(xo, yo, m0, sigma):
    """GP posterior on the grid and the log marginal likelihood of (xo, yo)."""
    yc = yo - m0
    K_go = kernel(xs, xo)
    S = kernel(xo, xo) + sigma**2 * np.eye(len(xo))
    L = np.linalg.cholesky(S)
    alpha = np.linalg.solve(S, yc)
    log_ml = -0.5 * yc @ alpha - np.log(np.diag(L)).sum() - 0.5 * len(xo) * np.log(2 * np.pi)
    return m0 + K_go @ alpha, kernel(xs, xs) - K_go @ np.linalg.solve(S, K_go.T), log_ml


def mode(xo, yo, m0, k):
    """Samples for one mode, its noise level marginalized on the grid, and its log evidence."""
    post = [gp(xo, yo, m0, s) for s in SIGMAS]
    logw = np.array([p[2] for p in post])
    cdf = np.cumsum(np.exp(logw - logsumexp(logw)))
    means, sigmas = [], []
    for h in range(len(COLORS)):
        i = min(np.searchsorted(cdf, u[h, k]), len(SIGMAS) - 1)
        m, C, _ = post[i]
        means.append(m + np.linalg.cholesky(C + 1e-8 * np.eye(len(xs))) @ z[h, k])
        sigmas.append(SIGMAS[i])
    return np.array(means), np.array(sigmas), logsumexp(logw) - np.log(len(SIGMAS))


single = mode(x_obs, y_obs, 0.0, 0)
left, right = (np.sign(y_obs) == s for s in (-1, 1))
modes = [mode(x_obs[left], y_obs[left], -0.15, 0), mode(x_obs[right], y_obs[right], 0.15, 1)]
pr = p_right(x_obs)
evidence_mixture = (modes[0][2] + modes[1][2] + np.log(1 - pr[left]).sum()
                    + np.log(pr[right]).sum())
evidence_single = single[2]
print(f"log evidence: one Gaussian {evidence_single:.1f}, mixture {evidence_mixture:.1f}")


def mixture_outline(n=300):
    t = np.linspace(0, 2 * np.pi, n)
    r = 1 + 0.07 * np.sin(2 * t + 0.6) + 0.05 * np.cos(3 * t + 0.9)
    return 0.05 + 0.62 * r * np.cos(t), -0.05 + 1.1 * r * np.sin(t)


def draw_space(ax, outline, centre, cov):
    style_space_axes(ax)
    ax.set_ylim(-1.9, 1.9)
    bx, by = space_outline()
    ax.fill(bx, by, color=SPACE, lw=0, zorder=0)
    ax.plot(bx, by, color=POINT, lw=1.2, zorder=1)
    mx, my = outline
    ax.fill(mx, my, color=MODEL, alpha=0.12, lw=0, zorder=1)
    ax.plot(mx, my, color=MODEL, lw=1.6, zorder=3)
    draw_truth_star(ax, label=False)
    gx, gy = np.meshgrid(np.linspace(-1, 1, 200), np.linspace(-1.9, 1.9, 380))
    diff = np.stack([gx - centre[0], gy - centre[1]], axis=-1)
    dens = np.exp(-0.5 * np.einsum("...i,ij,...j->...", diff, np.linalg.inv(cov), diff))
    rgba = np.zeros((*gx.shape, 4))
    rgba[..., :3] = to_rgb(MODEL)
    rgba[..., 3] = 0.75 * dens
    shade = ax.imshow(rgba, origin="lower", extent=(-1, 1, -1.9, 1.9), aspect="auto",
                      interpolation="bilinear", zorder=2)
    shade.set_clip_path(Polygon(np.column_stack(outline), transform=ax.transData))
    dots = np.random.default_rng(1).multivariate_normal(centre, cov, len(COLORS))
    inside = Polygon(np.column_stack(outline)).get_path().contains_points(dots)
    dots[~inside] = centre + 0.5 * (dots[~inside] - centre)
    ax.scatter(*dots.T, s=40, c=COLORS, ec="white", lw=0.8, zorder=5)


def draw_curves(ax, means, sigmas, fades, band=0.1):
    style_data_axes(ax)
    ax.set_ylabel("")
    ax.set_xticks([c for c, _ in LANES], ["left", "middle", "right"], fontsize=14, color=INK2)
    ax.tick_params(axis="x", length=3, color=POINT)
    for h, color in enumerate(COLORS):
        for m, sd, fade in zip(means[h], sigmas[h], fades):
            for lo in range(len(xs) - 1):
                seg = slice(lo, lo + 2)
                ax.fill_between(xs[seg], m[seg] - 2 * sd, m[seg] + 2 * sd, color=color,
                                alpha=band * fade[lo], lw=0, zorder=1.1)
                ax.plot(xs[seg], m[seg], color=color, lw=1.8, alpha=0.9 * fade[lo], zorder=1.2,
                        solid_capstyle="butt")
    ax.scatter(x_obs[:150], y_obs[:150], s=8, color=INK2, alpha=0.7, lw=0, zorder=3)


setup_style()
fig = plt.figure(figsize=(11.5, 5.4), facecolor=SURFACE)
rows = ((0.53, "misspecified", evidence_single),
        (0.03, "well specified", evidence_mixture))

# The misspecified posterior concentrates where the model comes closest to the truth.
mx, my = model_outline()
mx, my = mx, my + 0.15
i = np.argmin(np.hypot(mx - TRUTH_XY[0], my - TRUTH_XY[1]))
best = np.array([mx[i], my[i]])
draw_space(fig.add_axes((0.0, 0.53, 0.18, 0.44)), (mx, my),
           best + 0.12 * (np.array([-0.1, -0.25]) - best), np.array([[0.04, 0.012], [0.012, 0.03]]))
draw_space(fig.add_axes((0.0, 0.03, 0.18, 0.44)), mixture_outline(),
           np.array(TRUTH_XY) - [0.03, 0.05], np.array([[0.03, 0.008], [0.008, 0.03]]))

flat = np.ones(len(xs) - 1)
mix = [np.clip(1.6 * (w[:-1] + w[1:]) / 2, 0.05, 1) for w in (1 - p_right(xs), p_right(xs))]
ax_top = fig.add_axes((0.25, 0.6, 0.5, 0.34))
draw_curves(ax_top, single[0][:, None], single[1][:, None], [flat], band=0.04)
ax_top.set_xticklabels([])
ax_bottom = fig.add_axes((0.25, 0.1, 0.5, 0.34))
draw_curves(ax_bottom, np.stack([modes[0][0], modes[1][0]], axis=1),
            np.stack([modes[0][1], modes[1][1]], axis=1), mix)
ax_bottom.set_xlabel("lane position $x$", fontsize=16, color=INK2, labelpad=4)

for ax, (_, label, ev) in zip((ax_top, ax_bottom), rows):
    ax.text(0, 1.05, label, transform=ax.transAxes, fontsize=17, color=INK2)
    ax.text(1.06, 0.5, r"$\log p(\mathcal{D} \mid \mathcal{M})$" f"\n$= {ev:.0f}$",
            transform=ax.transAxes, fontsize=17, color=INK2, va="center", linespacing=1.3)
    top = ax.get_xaxis_transform()
    ax.plot(GAP, [1.03, 1.03], color=POINT, lw=1.2, transform=top, clip_on=False)
    ax.text(np.mean(GAP), 1.06, "no data", transform=top, fontsize=15, color=INK2, ha="center")

for y, text in ((0.75, r"$\mathcal{N}(y;\, \mu,\, \sigma^2)$"),
                (0.25, r"$\pi\, \mathcal{N}(y;\, \mu_1,\, \sigma_1^2)$" "\n"
                       r"$+\, (1 - \pi)\, \mathcal{N}(y;\, \mu_2,\, \sigma_2^2)$")):
    fig.text(0.0, y, text, fontsize=19, color=MODEL, ha="right", va="center", linespacing=1.8)

save(fig, __file__)
