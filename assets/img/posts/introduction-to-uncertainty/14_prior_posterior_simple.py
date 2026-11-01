"""A few hypotheses drawn from the prior, then from the posterior after 20 points.

Each hypothesis is a mixture of two Gaussians whose mode curves have a Gaussian-process prior
and whose noise levels have a log-uniform prior. Gridding the noise level keeps both posteriors
exact.

Run: python 14_prior_posterior_simple.py  (requires numpy, scipy, matplotlib, pillow)
"""

import io
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import PolyCollection
from matplotlib.colors import to_rgb
from matplotlib.patches import Polygon
from PIL import Image

from common import (INK2, LANES, TRUTH, MODEL, POINT, SPACE, SURFACE, TRUTH_XY, X_LIM, draw_truth_star,
                    input_density, lane_modes, p_right, sample_inputs, sample_truth, setup_style,
                    space_outline, style_data_axes, style_space_axes)

N_DATA, MORPH = 20, 14
PRIOR_MEAN, PRIOR_STD, LENGTH = 0.15, 0.35, 0.3
SIGMAS = np.geomspace(0.04, 0.15, 60)
CENTRE = np.array([0.0, -0.15])
COLORS = ["#2a78d6", "#8b5cc9", "#17a07b", "#d6457f"]

MIDDLE_GAP = 0.3

# The data happen to miss the middle lane, so the hypotheses still disagree there.
data_rng = np.random.default_rng(2)
x_obs = sample_inputs(10 * N_DATA, data_rng)
x_obs, y_obs = sample_truth(N_DATA, data_rng, x_obs[np.abs(x_obs) > MIDDLE_GAP][:N_DATA])

rng = np.random.default_rng(2)
xs = np.linspace(*X_LIM, 160)
z = rng.standard_normal((len(COLORS), 2, len(xs)))
u = rng.uniform(0.05, 0.95, (len(COLORS), 2))


def kernel(a, b):
    return PRIOR_STD**2 * np.exp(-0.5 * ((a[:, None] - b[None, :]) / LENGTH) ** 2)


def mode_posterior(sign, sigma, data):
    m0 = sign * PRIOR_MEAN
    K_gg = kernel(xs, xs)
    if not data:
        return np.full_like(xs, m0), K_gg, 0.0
    keep = np.sign(y_obs) == sign
    xo, yo = x_obs[keep], y_obs[keep] - m0
    K_go = kernel(xs, xo)
    S = kernel(xo, xo) + sigma**2 * np.eye(len(xo))
    L = np.linalg.cholesky(S)
    alpha = np.linalg.solve(S, yo)
    log_ml = -0.5 * yo @ alpha - np.log(np.diag(L)).sum()
    return m0 + K_go @ alpha, K_gg - K_go @ np.linalg.solve(S, K_go.T), log_ml


def state(data):
    """Samples (means, sigmas) and the projected density components for one state."""
    means = np.empty((len(COLORS), 2, len(xs)))
    sigmas = np.empty((len(COLORS), 2))
    parts = []
    for k, sign in enumerate((-1, 1)):
        post = [mode_posterior(sign, s, data) for s in SIGMAS]
        logw = np.array([p[2] for p in post])
        w = np.exp(logw - logw.max())
        w /= w.sum()
        cdf = np.cumsum(w)
        for h in range(len(COLORS)):
            i = min(np.searchsorted(cdf, u[h, k]), len(SIGMAS) - 1)
            m, C, _ = post[i]
            means[h, k] = m + np.linalg.cholesky(C + 1e-8 * np.eye(len(xs))) @ z[h, k]
            sigmas[h, k] = SIGMAS[i]
        parts.append([(wi, m, C) for wi, (m, C, _) in zip(w, post) if wi > 1e-3])
    return means, sigmas, parts


# Random directions where a mode is actually used, corrected so the truth lands on the star.
truth = np.concatenate(lane_modes(xs))
prior_mean = np.concatenate([np.full_like(xs, -PRIOR_MEAN), np.full_like(xs, PRIOR_MEAN)])
relevance = np.concatenate([input_density(xs) * (1 - p_right(xs)), input_density(xs) * p_right(xs)])
relevance = np.sqrt(relevance / relevance.max())
d = truth - prior_mean
wd = relevance * d
B = rng.standard_normal((2, 2 * len(xs))) * relevance * 0.15
A = B + np.outer(np.array(TRUTH_XY) - CENTRE - B @ d, wd) / (wd @ d)
A_modes = (A[:, :len(xs)], A[:, len(xs):])


def project(f):
    return CENTRE + (f.ravel() - prior_mean) @ A.T


gx, gy = np.meshgrid(np.linspace(-1, 1, 300), np.linspace(-1.75, 1.45, 450))
extent = (-1, 1, -1.75, 1.45)


def density_image(parts):
    """The projected density: a mixture over the two modes' noise-level grids."""
    dens = np.zeros_like(gx)
    for wl, ml, Cl in parts[0]:
        for wr, mr, Cr in parts[1]:
            mean = project(np.stack([ml, mr]))
            cov = A_modes[0] @ Cl @ A_modes[0].T + A_modes[1] @ Cr @ A_modes[1].T
            diff = np.stack([gx - mean[0], gy - mean[1]], axis=-1)
            q = np.einsum("...i,ij,...j->...", diff, np.linalg.inv(cov), diff)
            dens += wl * wr * np.exp(-0.5 * q) / np.sqrt(np.linalg.det(cov))
    return dens


prior, post = state(False), state(True)
dens_prior, dens_post = density_image(prior[2]), density_image(post[2])
# Each state is scaled to its own peak: the shading shows relative plausibility.
dens_prior, dens_post = dens_prior / dens_prior.max(), dens_post / dens_post.max()


def mixture_outline(n=300):
    t = np.linspace(0, 2 * np.pi, n)
    r = 1 + 0.07 * np.sin(2 * t + 0.6) + 0.05 * np.cos(3 * t + 0.9)
    return 0.0 + 0.82 * r * np.cos(t), -0.15 + 1.45 * r * np.sin(t)


setup_style()
fig = plt.figure(figsize=(10.5, 5.2), facecolor=SURFACE)
ax_space = fig.add_axes((0.0, 0.04, 0.3, 0.84))
style_space_axes(ax_space)
bx, by = space_outline()
ax_space.fill(bx, by, color=SPACE, lw=0, zorder=0)
ax_space.plot(bx, by, color=POINT, lw=1.2, zorder=1)
mx, my = mixture_outline()
ax_space.plot(mx, my, color=MODEL, lw=1.6, zorder=4)
ax_space.text(0.0, -1.05, r"model $\{p_\theta\}$", fontsize=16, color=MODEL, ha="center",
              zorder=6)
ax_space.text(0, 2.05, "all conditional\n" r"distributions $p(y \mid x)$", fontsize=18,
              ha="center", va="bottom", color=INK2)
draw_truth_star(ax_space, label=False)
ax_space.text(0.15, TRUTH_XY[1] + 0.22, r"$p^*(y \mid x)$", fontsize=17, ha="center",
              va="bottom", zorder=6)
blob = Polygon(np.column_stack([mx, my]), transform=ax_space.transData)

ax_data = fig.add_axes((0.42, 0.2, 0.55, 0.66))
style_data_axes(ax_data)
ax_data.set_xticks([c for c, _ in LANES], ["left", "middle", "right"], fontsize=14, color=INK2)
ax_data.tick_params(axis="x", length=3, color=POINT)
ax_data.set_xlabel("lane position $x$", fontsize=17, color=INK2, labelpad=4)
title = ax_data.text(0, 1.04, "", transform=ax_data.transAxes, fontsize=18, color=INK2)

# As in the MDN figures, fade each mode where the mixture gives it little weight.
mix = (1 - p_right(xs), p_right(xs))
fade = [np.clip(1.6 * (w[:-1] + w[1:]) / 2, 0.05, 1) for w in mix]
# Bayes reweights hypotheses rather than moving them, so the prior's samples fade out where they
# are and the posterior's fade in where they are.
curves = []
for means, sigmas in (prior[:2], post[:2]):
    for h, color in enumerate(COLORS):
        for k in range(2):
            m, sd = means[h, k], sigmas[h, k]
            lo, hi = m - 2 * sd, m + 2 * sd
            band = PolyCollection(np.stack([np.column_stack([xs[:-1], lo[:-1]]),
                                            np.column_stack([xs[1:], lo[1:]]),
                                            np.column_stack([xs[1:], hi[1:]]),
                                            np.column_stack([xs[:-1], hi[:-1]])], axis=1),
                                  lw=0, zorder=1.1)
            line = PolyCollection(np.stack([np.column_stack([xs[:-1], m[:-1]]),
                                            np.column_stack([xs[1:], m[1:]])], axis=1),
                                  facecolors="none", lw=2, zorder=1.2, closed=False)
            ax_data.add_collection(band)
            ax_data.add_collection(line)
            curves.append((band, line, to_rgb(color), fade[k]))
scatter = ax_data.scatter(x_obs, y_obs, s=24, color=INK2, lw=0, zorder=3)
dot_sets = [ax_space.scatter(*np.array([project(means[h]) for h in range(len(COLORS))]).T, s=60,
                             c=COLORS, ec="white", lw=1, zorder=5) for means, _ in (prior[:2], post[:2])]
shade = ax_space.imshow(np.zeros((*gx.shape, 4)), origin="lower", extent=extent, aspect="auto",
                        interpolation="bilinear", zorder=2)
shade.set_clip_path(blob)


def draw(s):
    """s = 0 shows the prior, s = 1 the posterior; in between, a cross-fade of the two."""
    n = len(curves) // 2
    for i, (band, line, rgb, a) in enumerate(curves):
        w = 1 - s if i < n else s
        band.set_facecolors([(*rgb, 0.13 * w * ai) for ai in a])
        line.set_edgecolors([(*rgb, 0.9 * w * ai) for ai in a])
    dot_sets[0].set_alpha(1 - s)
    dot_sets[1].set_alpha(s)
    dens = (1 - s) * dens_prior + s * dens_post
    rgba = np.zeros((*gx.shape, 4))
    rgba[..., :3] = to_rgb(MODEL)
    rgba[..., 3] = 0.55 * dens**0.5
    shade.set_data(rgba)
    scatter.set_alpha(s)
    title.set_text("no data" if s < 0.5 else f"$n = {N_DATA}$")


frames = []


def grab():
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=110, facecolor=SURFACE, bbox_inches="tight",
                pad_inches=0.05)
    frames.append(Image.open(buf).convert("RGB"))


steps = [0] + [0.5 - 0.5 * np.cos(np.pi * t / MORPH) for t in range(1, MORPH + 1)]
for s in steps:
    draw(s)
    grab()
    if s == 0:
        fig.savefig(Path(__file__).with_name(Path(__file__).stem + "_prior.png"), dpi=200,
                    facecolor=SURFACE, bbox_inches="tight", pad_inches=0.05)
fig.savefig(Path(__file__).with_suffix(".png"), dpi=200, facecolor=SURFACE,
            bbox_inches="tight", pad_inches=0.05)
durations = [3000] + [90] * (MORPH - 1) + [6000]
# One palette for all frames; per-frame palettes can drop the orange of the star.
sheet = Image.new("RGB", (frames[0].width, 3 * frames[0].height))
for i, f in enumerate((frames[0], frames[MORPH // 2], frames[-1])):
    sheet.paste(f, (0, i * f.height))
keys = [TRUTH, MODEL, INK2, SURFACE, *COLORS]
palette = sheet.quantize(256 - len(keys))
colors = palette.getpalette()[:3 * (256 - len(keys))]
colors += [round(255 * c) for key in keys for c in to_rgb(key)]
palette.putpalette(colors)
frames = [f.quantize(palette=palette) for f in frames]
frames[0].save(Path(__file__).with_suffix(".gif"), save_all=True, append_images=frames[1:],
               duration=durations, loop=0)
