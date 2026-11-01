"""Shared style, ground truth and hypothesis-space geometry for the figures."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import ConnectionPatch
from matplotlib.colors import LinearSegmentedColormap, to_rgb
from scipy.stats import norm

SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK2 = "#52514e"
POINT = "#a9a8a3"
SPACE = "#f1f0ec"
TRUTH = "#d9822b"
MODEL = "#2a78d6"
MODEL_PALE = "#cde2fb"
FONT = "Helvetica Neue"

X_LIM = (-1.6, 1.6)
Y_LIM = (-0.85, 0.85)
ROAD = (-1, 1)
LANES = ((-0.62, 1.0), (0.0, 0.8), (0.62, 0.9))  # (center, relative traffic)
OFF_ROAD = "#e9e7e1"


def setup_style():
    plt.rcParams.update({"font.family": FONT, "font.size": 10, "axes.edgecolor": INK2,
                         "axes.labelcolor": INK2, "xtick.color": INK, "text.color": INK,
                         "mathtext.fontset": "cm"})


def density_cmap(color):
    return LinearSegmentedColormap.from_list("d", [SURFACE, color])


# Lane-split example: x is the car's lateral offset from the divider just before the split,
# y the steering angle (negative = left). Off the road, p(x) = 0.
TRUE_STD = 0.07


def lane_modes(x):
    return -0.45 + 0.08 * x, 0.45 + 0.08 * x


def p_right(x):
    return 1 / (1 + np.exp(-x / 0.3))


def _input_shape(x):
    lanes = sum(h * np.exp(-(((x - c) / 0.14) ** 2)) for c, h in LANES)
    return lanes + 0.04 * (1 - x**2)


_xs = np.linspace(*ROAD, 2001)
_INPUT_NORM = np.sum(_input_shape(_xs)) * (_xs[1] - _xs[0])
_INPUT_MAX = _input_shape(_xs).max()


def input_density(x):
    inside = (x > ROAD[0]) & (x < ROAD[1])
    return np.where(inside, _input_shape(x) / _INPUT_NORM, 0.0)


def true_density(x, y):
    left, right = lane_modes(x)
    w = p_right(x)
    d = (1 - w) * norm.pdf(y, left, TRUE_STD) + w * norm.pdf(y, right, TRUE_STD)
    return np.where(input_density(x) > 0, d, 0.0)


def sample_inputs(n, rng):
    x = np.empty(0)
    while len(x) < n:
        c = rng.uniform(*ROAD, 4 * n)
        x = np.concatenate([x, c[rng.uniform(0, _INPUT_MAX, len(c)) < _input_shape(c)]])
    return x[:n]


def sample_truth(n, rng, x=None):
    x = sample_inputs(n, rng) if x is None else x
    left, right = lane_modes(x)
    y = np.where(rng.uniform(0, 1, len(x)) < p_right(x), right, left)
    return x, y + TRUE_STD * rng.standard_normal(len(x))


def space_outline(n=400):
    """A smooth irregular closed curve standing in for the space of all p(y|x)."""
    t = np.linspace(0, 2 * np.pi, n)
    r = 1 + 0.07 * np.sin(2 * t + 0.4) + 0.05 * np.cos(3 * t + 1.1) + 0.03 * np.sin(5 * t)
    return 0.95 * r * np.cos(t), 1.8 * r * np.sin(t)


TRUTH_XY = (0.3, 0.56)


def style_space_axes(ax):
    ax.set_facecolor(SURFACE)
    ax.set_aspect("equal")
    ax.set_xlim(-1.15, 1.15)
    ax.set_ylim(-2.0, 2.6)
    ax.axis("off")


def _shade_off_road(ax):
    for lo, hi in ((X_LIM[0], ROAD[0]), (ROAD[1], X_LIM[1])):
        ax.axvspan(lo, hi, color=OFF_ROAD, alpha=0.85, lw=0, zorder=1.5)


def style_data_axes(ax):
    ax.set_facecolor(SURFACE)
    ax.set_xlim(*X_LIM)
    ax.set_ylim(*Y_LIM)
    ax.set_xticks([])
    ax.set_yticks([-0.45, 0.45], ["left", "right"], fontsize=15, color=INK2)
    ax.tick_params(axis="y", length=0, pad=6)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(POINT)
    ax.set_ylabel("steering angle $y$", fontsize=17, color=INK2, labelpad=2)
    _shade_off_road(ax)
    for x in (np.mean((X_LIM[0], ROAD[0])), np.mean((ROAD[1], X_LIM[1]))):
        ax.text(x, 0, "off road", rotation=90, ha="center", va="center", fontsize=15,
                color=POINT, zorder=2)


def draw_input_density(ax, color=INK2):
    """A strip below the data panel showing p(x)."""
    xs = np.linspace(*X_LIM, 600)
    px = input_density(xs)
    ax.set_facecolor(SURFACE)
    _shade_off_road(ax)
    ax.fill_between(xs, 0, px, color=color, alpha=0.25, lw=0, zorder=1)
    ax.plot(xs, px, color=color, lw=1.2, zorder=2)
    ax.set_xlim(*X_LIM)
    ax.set_ylim(0, px.max() * 1.15)
    ax.set_yticks([])
    ax.set_xticks([c for c, _ in LANES], ["left", "middle", "right"], fontsize=14, color=INK2)
    ax.tick_params(axis="x", length=3, color=POINT)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(POINT)
    ax.set_ylabel("$p(x)$", fontsize=18, color=INK2, rotation=0, ha="right", va="center")
    ax.set_xlabel("lane position $x$", fontsize=17, color=INK2, labelpad=4)


def draw_density(ax, density_fn, color, extent=None, alpha=1.0, gamma=0.6, zorder=0):
    """Density as a transparent overlay, so shading underneath stays visible."""
    extent = extent or (*X_LIM, *Y_LIM)
    xs = np.linspace(extent[0], extent[1], 300)
    ys = np.linspace(extent[2], extent[3], 300)
    X, Y = np.meshgrid(xs, ys)
    D = density_fn(X, Y)
    D = (D / D.max()) ** gamma
    rgba = np.zeros((*D.shape, 4))
    rgba[..., :3] = to_rgb(color)
    rgba[..., 3] = alpha * D
    ax.imshow(rgba, origin="lower", extent=extent, aspect="auto", interpolation="bilinear",
              zorder=zorder)


def draw_steering_wheel(fig, rect, color=INK2):
    from matplotlib.patches import Circle, Polygon, Wedge

    ax = fig.add_axes(rect)
    ax.set_aspect("equal")
    ax.set_xlim(-1.05, 1.05)
    ax.set_ylim(-1.05, 1.05)
    ax.axis("off")
    ax.add_patch(Wedge((0, 0), 1.0, 0, 360, width=0.2, color=color))
    # Spokes taper from the hub to the rim; the side spokes droop slightly, as on a real wheel.
    for angle, w_hub, w_rim in ((-10, 0.2, 0.32), (190, 0.2, 0.32), (-90, 0.26, 0.4)):
        t = np.deg2rad(angle)
        d, n = np.array([np.cos(t), np.sin(t)]), np.array([-np.sin(t), np.cos(t)])
        hub, rim = 0.25 * d, 0.88 * d
        ax.add_patch(Polygon([hub + n * w_hub / 2, rim + n * w_rim / 2, rim - n * w_rim / 2,
                              hub - n * w_hub / 2], color=color, lw=0))
    ax.add_patch(Circle((0, -0.05), 0.33, color=color))
    ax.add_patch(Circle((0, -0.05), 0.13, color=SURFACE))
    return ax


def make_layout():
    """The shared two-panel layout: hypothesis space left, data and p(x) right."""
    setup_style()
    fig = plt.figure(figsize=(8.4, 6.4), facecolor=SURFACE)
    ax_space = fig.add_axes((0.0, 0.02, 0.38, 0.9))
    ax_data = fig.add_axes((0.53, 0.34, 0.45, 0.58))
    ax_px = fig.add_axes((0.53, 0.12, 0.45, 0.14))
    style_space_axes(ax_space)
    style_data_axes(ax_data)
    draw_input_density(ax_px)
    draw_steering_wheel(fig, (0.445, 0.335, 0.065, 0.065))

    bx, by = space_outline()
    ax_space.fill(bx, by, color=SPACE, lw=0, zorder=0)
    ax_space.plot(bx, by, color=POINT, lw=1.2, zorder=1)
    ax_space.text(0, 2.05, "all conditional\n" r"distributions $p(y \mid x)$", fontsize=18,
                  ha="center", va="bottom", color=INK2)
    return fig, ax_space, ax_data, ax_px


def draw_truth_star(ax_space, label=True, label_above=False):
    ax_space.plot(*TRUTH_XY, marker="*", ms=26, color=TRUTH, mec=INK, mew=0.6, zorder=6)
    if label:
        dy, va = (0.15, "bottom") if label_above else (-0.15, "top")
        ax_space.text(TRUTH_XY[0], TRUTH_XY[1] + dy, r"$p^*(y \mid x)$", fontsize=20,
                      color=INK, va=va, ha="center", zorder=6)


def link(fig, ax_space, xy, ax_data, color, xy_data=(0.02, 0.97), rad=-0.15):
    fig.add_artist(ConnectionPatch(xyA=xy, coordsA=ax_space.transData, xyB=xy_data,
                                   coordsB=ax_data.transAxes, color=color, lw=1.4,
                                   ls=(0, (4, 3)), connectionstyle=f"arc3,rad={rad}"))


def save(fig, script):
    fig.savefig(Path(script).with_suffix(".png"), dpi=200, facecolor=SURFACE,
                bbox_inches="tight", pad_inches=0.05)


# Linear-Gaussian model: theta = (intercept, slope), fixed std. It cannot represent the truth.
MODEL_STD = 0.05


def model_outline(n=300):
    """A smooth blob inside the space for the model's hypotheses; it excludes the truth."""
    t = np.linspace(0, 2 * np.pi, n)
    r = 1 + 0.08 * np.sin(2 * t + 1.0) + 0.05 * np.cos(3 * t + 0.3)
    return -0.1 + 0.62 * r * np.cos(t), -0.75 + 0.68 * r * np.sin(t)


def draw_model_blob(ax_space, label=r"model $\{p_\theta\}$"):
    bx, by = model_outline()
    ax_space.fill(bx, by, color=MODEL_PALE, alpha=0.8, lw=0, zorder=2)
    ax_space.plot(bx, by, color=MODEL, lw=1.6, zorder=3)
    ax_space.text(-0.1, -1.08, label, fontsize=18, color=MODEL, ha="center",
                  va="center", zorder=6)


def draw_linear_hypothesis(ax, theta, color=MODEL, alpha=1.0, band=True):
    a, b = theta
    xs = np.linspace(*X_LIM, 200)
    mu = a + b * xs
    if band:
        ax.fill_between(xs, mu - 2 * MODEL_STD, mu + 2 * MODEL_STD, color=color,
                        alpha=0.25 * alpha, lw=0, zorder=1)
    ax.plot(xs, mu, color=color, lw=2.2, alpha=alpha, zorder=1)
