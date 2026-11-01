"""Reserve planning example, shared by figures 20 to 22.

y is the shortfall: how much less wind power arrives than planned. The truth has rare large
drops (ramps) on top of ordinary forecast error. The model is the Gaussian that fits it best
by likelihood, i.e. with matched mean and variance.
"""

import numpy as np
from scipy.optimize import brentq
from scipy.stats import norm

from common import INK2, POINT, SURFACE

W_RAMP, MU_RAMP, STD_RAMP = 0.03, 3.5, 1.2

MODEL_MEAN = W_RAMP * MU_RAMP
MODEL_STD = np.sqrt((1 - W_RAMP) + W_RAMP * (STD_RAMP**2 + MU_RAMP**2) - MODEL_MEAN**2)


def true_pdf(y):
    return (1 - W_RAMP) * norm.pdf(y) + W_RAMP * norm.pdf(y, MU_RAMP, STD_RAMP)


def true_sf(y):
    return (1 - W_RAMP) * norm.sf(y) + W_RAMP * norm.sf(y, MU_RAMP, STD_RAMP)


def true_quantile(tau):
    return brentq(lambda y: true_sf(y) - (1 - tau), -10, 20)


def model_pdf(y):
    return norm.pdf(y, MODEL_MEAN, MODEL_STD)


def model_sf(y):
    return norm.sf(y, MODEL_MEAN, MODEL_STD)


def model_quantile(tau):
    return norm.ppf(tau, MODEL_MEAN, MODEL_STD)


def sample_truth(n, rng):
    ramp = rng.uniform(size=n) < W_RAMP
    return np.where(ramp, rng.normal(MU_RAMP, STD_RAMP, n), rng.standard_normal(n))


def style_exceedance_axes(ax, ys):
    ax.set_facecolor(SURFACE)
    ax.set_yscale("log")
    ax.set_xlim(ys[0], ys[-1])
    ax.set_ylim(5e-4, 0.7)
    ax.set_yticks([0.5, 0.1, 0.01, 0.001], ["1 in 2", "1 in 10", "1 in 100", "1 in 1000"],
                  fontsize=14, color=INK2)
    ax.minorticks_off()
    ax.set_xticks([])
    ax.tick_params(axis="y", length=0, pad=6)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(POINT)
    ax.set_xlabel("reserve", fontsize=17, color=INK2)
    ax.set_ylabel("chance of a shortage", fontsize=17, color=INK2)
