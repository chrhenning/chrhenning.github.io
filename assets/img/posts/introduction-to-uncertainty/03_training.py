"""Training a small network with a Gaussian likelihood of fixed variance (i.e., MSE).

The mean converges, the fixed variance stays, and the expected KL to the truth stalls above
zero because the truth lies outside the model.

Run: python 03_training.py  (requires numpy, scipy, matplotlib, pillow)
"""

import io
from pathlib import Path

import numpy as np
from PIL import Image

from common import (INK2, MODEL, MODEL_STD, POINT, ROAD, SURFACE, TRUTH_XY, X_LIM,
                    draw_model_blob, draw_truth_star, input_density, lane_modes, make_layout,
                    model_outline, p_right, sample_truth, true_density)

rng = np.random.default_rng(0)
HIDDEN, STEPS, LR = 32, 250, 0.0002
INIT_LINE = (0.15, 0.25)  # matches p_theta0 in figure 02
INIT_XY = (-0.3, -0.45)


def forward(params, x):
    W1, b1, W2, b2 = params
    h = np.tanh(np.outer(x, W1) + b1)
    return h @ W2 + b2, h


def adam(params, x, y, steps, lr, on_step=None):
    m = [np.zeros_like(p) for p in params]
    v = [np.zeros_like(p) for p in params]
    for t in range(1, steps + 1):
        f, h = forward(params, x)
        r = 2 * (f - y) / len(x)
        dh = np.outer(r, params[2]) * (1 - h**2)
        grads = [dh.T @ x, dh.sum(0), h.T @ r, r.sum()]
        for i, g in enumerate(grads):
            m[i] = 0.9 * m[i] + 0.1 * g
            v[i] = 0.999 * v[i] + 0.001 * g**2
            params[i] = params[i] - lr * (m[i] / (1 - 0.9**t)) / (np.sqrt(v[i] / (1 - 0.999**t)) + 1e-8)
        if on_step:
            on_step(t, params)
    return params


# Expected KL(p* || p_theta) over p(x), computed on a grid. The model's NLL depends on the mean
# only through E[(y - f(x))^2], which is why minimizing it is the same as minimizing the MSE.
xg = np.linspace(*ROAD, 401)[1:-1]
px = input_density(xg)
px /= px.sum()
yg = np.linspace(-1.5, 1.5, 3001)
P = true_density(xg[:, None], yg[None, :])
neg_entropy = np.sum(P * np.log(np.maximum(P, 1e-300)), axis=1) * (yg[1] - yg[0])
left, right = lane_modes(xg)
w = p_right(xg)


def expected_kl(f):
    second_moment = (1 - w) * (left - f) ** 2 + w * (right - f) ** 2 + 0.07**2
    kl = neg_entropy + 0.5 * np.log(2 * np.pi * MODEL_STD**2) + second_moment / (2 * MODEL_STD**2)
    return np.sum(px * kl)


x_train, y_train = sample_truth(20000, rng)
params = [rng.normal(0, 1.5, HIDDEN), rng.normal(0, 1.0, HIDDEN),
          rng.normal(0, 0.3 / np.sqrt(HIDDEN), HIDDEN), 0.0]
x_line = np.linspace(*X_LIM, 200)
params = adam(params, x_line, INIT_LINE[0] + INIT_LINE[1] * x_line, 1500, 0.01)

frame_steps = set(np.unique(np.linspace(0, STEPS, 60).astype(int)))
snapshots = {}
snapshots[0] = [p.copy() if isinstance(p, np.ndarray) else p for p in params]
adam(params, x_train, y_train, STEPS, LR,
     on_step=lambda t, p: snapshots.__setitem__(t, [q.copy() if isinstance(q, np.ndarray) else q
                                                    for q in p]) if t in frame_steps else None)
steps = sorted(snapshots)
kls = [expected_kl(forward(snapshots[s], xg)[0]) for s in steps]

# Cartoon path in the space: from theta_0 to the model's point closest to the truth.
bx, by = model_outline()
i = np.argmin((bx - TRUTH_XY[0]) ** 2 + (by - TRUTH_XY[1]) ** 2)
centre = np.array([bx.mean(), by.mean()])
end = centre + 0.93 * (np.array([bx[i], by[i]]) - centre)
start = np.array(INIT_XY)
ctrl = (start + end) / 2 + np.array([0.15, -0.1])


def path(s):
    return (1 - s) ** 2 * start + 2 * (1 - s) * s * ctrl + s**2 * end


fig, ax_space, ax_data, ax_px = make_layout()
draw_model_blob(ax_space)
draw_truth_star(ax_space, label_above=True)
ax_space.plot(*INIT_XY, "o", ms=10, color="white", mec=MODEL, mew=1.5, zorder=6)
ax_space.text(INIT_XY[0], INIT_XY[1] - 0.1, r"$p_{\theta_0}$", fontsize=20, color=MODEL,
              ha="center", va="top", zorder=6)
(trail,) = ax_space.plot([], [], color=MODEL, lw=1.5, alpha=0.6, zorder=5)
(gap,) = ax_space.plot([], [], color=INK2, lw=1.2, ls=(0, (3, 2.5)), zorder=5)
(dot,) = ax_space.plot([], [], "o", ms=10, color=MODEL, mec="white", mew=1.2, zorder=7)
kl_text = ax_space.text(0, 0, "", fontsize=16, color=INK2, ha="right", va="center", zorder=7)

xs, ys = sample_truth(120, np.random.default_rng(0))
ax_data.scatter(xs, ys, s=16, color=INK2, alpha=0.8, lw=0, zorder=2)
ax_data.text(0, 1.04, r"model $p_\theta(y \mid x)$", transform=ax_data.transAxes, fontsize=18,
             color=MODEL)
(mean_line,) = ax_data.plot([], [], color=MODEL, lw=2.2, zorder=1)
nll_text = ax_data.text(1, 1.04, "", transform=ax_data.transAxes, fontsize=16, color=INK2,
                        ha="right")
band = None

frames = []
for k, (s, kl) in enumerate(zip(steps, kls)):
    progress = (kls[0] - kl) / (kls[0] - kls[-1])
    trail_pts = np.array([path(u) for u in np.linspace(0, max(progress, 0), 50)])
    pos = path(np.clip(progress, 0, 1))
    trail.set_data(trail_pts[:, 0], trail_pts[:, 1])
    dot.set_data([pos[0]], [pos[1]])
    gap.set_data([pos[0], TRUTH_XY[0]], [pos[1], TRUTH_XY[1]])
    mid = (pos + np.array(TRUTH_XY)) / 2
    kl_text.set_position((mid[0] - 0.08, mid[1]))
    kl_text.set_text(f"KL = {kl:.1f}")

    # What we actually observe: the NLL on the training data, in nats per sample.
    resid = y_train - forward(snapshots[s], x_train)[0]
    nll = np.mean(resid**2) / (2 * MODEL_STD**2) + 0.5 * np.log(2 * np.pi * MODEL_STD**2)
    nll_text.set_text(f"NLL = {nll:.1f}")

    f = forward(snapshots[s], x_line)[0]
    mean_line.set_data(x_line, f)
    if band is not None:
        band.remove()
    band = ax_data.fill_between(x_line, f - 2 * MODEL_STD, f + 2 * MODEL_STD, color=MODEL,
                                alpha=0.25, lw=0, zorder=1)

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=110, facecolor=SURFACE, bbox_inches="tight",
                pad_inches=0.05)
    frames.append(Image.open(buf).convert("RGB"))
    if k == len(steps) - 1:
        fig.savefig(Path(__file__).with_suffix(".png"), dpi=200, facecolor=SURFACE,
                    bbox_inches="tight", pad_inches=0.05)

durations = [2500] + [110] * (len(frames) - 2) + [3000]
frames[0].save(Path(__file__).with_suffix(".gif"), save_all=True, append_images=frames[1:],
               duration=durations, loop=0)
print(f"expected KL: start {kls[0]:.1f}, end {kls[-1]:.1f}; final NLL {nll:.2f}; H(p*) {-np.sum(px * neg_entropy):.2f}")
