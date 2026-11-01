"""A small mixture density network (two Gaussians), trained with hand-written gradients."""

import numpy as np

from common import MODEL, X_LIM, sample_truth

K, HIDDEN = 2, 32
MIN_LOG_STD = np.log(0.03)


def init(rng):
    return [rng.normal(0, 1.5, (1, HIDDEN)), rng.normal(0, 1.0, HIDDEN),
            rng.normal(0, 0.3 / np.sqrt(HIDDEN), (HIDDEN, 3 * K)),
            np.array([0.0] * K + [-0.4, 0.4] + [np.log(0.15)] * K)]


def forward(params, x):
    W1, b1, W2, b2 = params
    h = np.tanh(x[:, None] @ W1 + b1)
    out = h @ W2 + b2
    logits, mu, log_std = out[:, :K], out[:, K:2 * K], out[:, 2 * K:]
    log_std = MIN_LOG_STD + np.logaddexp(0, log_std - MIN_LOG_STD)
    return logits, mu, log_std, h, out


def log_components(params, x, y):
    logits, mu, log_std, h, out = forward(params, x)
    log_pi = logits - np.logaddexp.reduce(logits, axis=1, keepdims=True)
    z = (y[:, None] - mu) / np.exp(log_std)
    return log_pi - 0.5 * z**2 - log_std - 0.5 * np.log(2 * np.pi), log_pi, z, h, out


def train(params, x, y, steps, lr, weight_decay):
    m = [np.zeros_like(p) for p in params]
    v = [np.zeros_like(p) for p in params]
    for t in range(1, steps + 1):
        lc, log_pi, z, h, out = log_components(params, x, y)
        gamma = np.exp(lc - np.logaddexp.reduce(lc, axis=1, keepdims=True))
        raw = out[:, 2 * K:]
        d_out = np.concatenate([np.exp(log_pi) - gamma,
                                -gamma * z / np.exp(forward(params, x)[2]),
                                gamma * (1 - z**2) / (1 + np.exp(-(raw - MIN_LOG_STD)))],
                               axis=1) / len(x)
        dh = d_out @ params[2].T * (1 - h**2)
        grads = [x[None, :] @ dh, dh.sum(0), h.T @ d_out, d_out.sum(0)]
        grads = [g + weight_decay * p for g, p in zip(grads, params)]
        for i, g in enumerate(grads):
            m[i] = 0.9 * m[i] + 0.1 * g
            v[i] = 0.999 * v[i] + 0.001 * g**2
            params[i] = params[i] - lr * (m[i] / (1 - 0.9**t)) / (np.sqrt(v[i] / (1 - 0.999**t)) + 1e-8)
    return params


def model_density(params, x, y):
    lc = log_components(params, x, y)[0]
    return np.exp(np.logaddexp.reduce(lc, axis=1))


def fit(n, seed):
    rng = np.random.default_rng(seed)
    x, y = sample_truth(n, rng)
    params = train(init(rng), x, y, 3000, 0.01, 1e-3)
    return x, y, params


def draw_fit(ax, params):
    xs = np.linspace(*X_LIM, 300)
    logits, mu, log_std, *_ = forward(params, xs)
    pi = np.exp(logits - np.logaddexp.reduce(logits, axis=1, keepdims=True))
    for k in range(K):
        # Fade each component where the network gives it little weight.
        for lo, hi in zip(range(0, len(xs) - 1), range(1, len(xs))):
            a = float(np.clip(pi[lo, k] * 1.6, 0.05, 1))
            seg = slice(lo, hi + 1)
            ax.fill_between(xs[seg], mu[seg, k] - 2 * np.exp(log_std[seg, k]),
                            mu[seg, k] + 2 * np.exp(log_std[seg, k]), color=MODEL,
                            alpha=0.22 * a, lw=0, zorder=1)
            ax.plot(xs[seg], mu[seg, k], color=MODEL, lw=2.2, alpha=a, zorder=1,
                    solid_capstyle="butt")
