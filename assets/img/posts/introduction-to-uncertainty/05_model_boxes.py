"""The two models as black boxes, one Gaussian versus a mixture of two.

Run: python 05_model_boxes.py  (requires numpy, matplotlib)
"""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

from common import INK, INK2, MODEL, MODEL_PALE, POINT, SURFACE, save, setup_style

setup_style()
fig, axes = plt.subplots(1, 2, figsize=(11, 4.4), facecolor=SURFACE)
fig.subplots_adjust(left=0, right=1, top=1, bottom=0, wspace=0.08)


def arrow(ax, a, b):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=14, color=INK2,
                                 lw=1.4, shrinkA=0, shrinkB=0))


def black_box(ax, title, outputs, formula):
    ax.set_facecolor(SURFACE)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis("off")
    ax.text(5, 6.6, title, fontsize=19, color=INK2, ha="center", va="center")

    ax.text(0.9, 3.9, "$x$", fontsize=24, color=INK, ha="center", va="center")
    arrow(ax, (1.3, 3.9), (2.8, 3.9))
    ax.add_patch(FancyBboxPatch((2.9, 2.7), 2.6, 2.4, boxstyle="round,pad=0,rounding_size=0.3",
                                fc=MODEL_PALE, ec=MODEL, lw=1.8))
    ax.text(4.2, 3.9, r"$f_\theta$", fontsize=28, color=MODEL, ha="center", va="center")

    ys = [3.9] if len(outputs) == 1 else [3.9 + 0.62 * (2 - i) for i in range(len(outputs))]
    for label, y in zip(outputs, ys):
        arrow(ax, (5.6, 3.9 + (y - 3.9) * 0.35), (7.1, y))
        ax.text(7.3, y, label, fontsize=21, color=MODEL, ha="left", va="center")

    colored_math(ax, 5, 1.0, formula, fontsize=17)


def colored_math(ax, x, y, parts, fontsize):
    """Mathtext cannot colour sub-expressions, so lay out coloured pieces side by side."""
    renderer = fig.canvas.get_renderer()
    texts = [ax.text(0, y, p, fontsize=fontsize, color=c, va="center") for p, c in parts]
    to_data = ax.transData.inverted()
    widths = [to_data.transform((t.get_window_extent(renderer).width, 0))[0]
              - to_data.transform((0, 0))[0] for t in texts]
    left = x - sum(widths) / 2
    for t, w in zip(texts, widths):
        t.set_x(left)
        left += w


black_box(axes[0], "one Gaussian, fixed variance", [r"$\mu$"],
          [(r"$p_\theta(y \mid x) = \mathcal{N}(y;\,$", INK), (r"$\mu$", MODEL),
           (r"$,\, \sigma^2)$", INK)])
black_box(axes[1], "mixture of two Gaussians",
          [r"$\pi$", r"$\mu_1$", r"$\mu_2$", r"$\sigma_1$", r"$\sigma_2$"],
          [(r"$p_\theta(y \mid x) =\,$", INK), (r"$\pi$", MODEL), (r"$\,\mathcal{N}(y;\,$", INK),
           (r"$\mu_1$", MODEL), (r"$,\,$", INK), (r"$\sigma_1^2$", MODEL),
           (r"$) + (1 -$", INK), (r"$\pi$", MODEL), (r"$)\,\mathcal{N}(y;\,$", INK),
           (r"$\mu_2$", MODEL), (r"$,\,$", INK), (r"$\sigma_2^2$", MODEL), (r"$)$", INK)])
fig.add_artist(plt.Line2D([0.5, 0.5], [0.08, 0.92], color=POINT, lw=1))

save(fig, __file__)
