"""Split conformal prediction on the lane-split example, shared by figures 18 and 19."""

import numpy as np
from scipy.stats import norm

from common import lane_modes, p_right, sample_truth
from mdn import fit, forward, model_density

ALPHA = 0.1


def mse_fit(x):
    # The best a fixed-variance Gaussian can do: the conditional mean.
    left, right = lane_modes(x)
    w = p_right(x)
    return (1 - w) * left + w * right


def mixture_cdf(params, x, y):
    logits, mu, log_std, *_ = forward(params, x)
    pi = np.exp(logits - np.logaddexp.reduce(logits, axis=1, keepdims=True))
    return (pi * norm.cdf((y[:, None] - mu) / np.exp(log_std))).sum(1)


def quantile(scores):
    n = len(scores)
    return np.sort(scores)[int(np.ceil((n + 1) * (1 - ALPHA))) - 1]


def calibrate(n=2000, seed=1):
    """Returns the mixture fit, the calibration data, and a threshold per score."""
    _, _, params = fit(2000, 0)
    xc, yc = sample_truth(n, np.random.default_rng(seed))
    scores = {"mse": np.abs(yc - mse_fit(xc)),
              "cdf": np.abs(mixture_cdf(params, xc, yc) - 0.5),
              "density": -model_density(params, xc, yc)}
    return params, xc, yc, scores, {k: quantile(s) for k, s in scores.items()}
