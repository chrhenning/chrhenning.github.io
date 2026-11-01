"""Sensor fusion in bird's-eye view: a camera is precise in direction but poor in depth, a radar
the opposite. Weighting each by its uncertainty (a product of Gaussians) gives a small fused estimate.

Run: python 11_sensor_fusion.py  (requires numpy, scipy, matplotlib)
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse, Polygon

from common import INK2, MODEL, POINT, SURFACE, TRUTH, save, setup_style

BEARING = np.deg2rad(18)
RANGE = 7.0
SIGHT = np.array([np.sin(BEARING), np.cos(BEARING)])
ACROSS = np.array([np.cos(BEARING), -np.sin(BEARING)])


def covariance(std_along, std_across):
    R = np.column_stack([SIGHT, ACROSS])
    return R @ np.diag([std_along**2, std_across**2]) @ R.T


def draw_ellipse(ax, mean, cov, color, fill_alpha, lw):
    vals, vecs = np.linalg.eigh(cov)
    angle = np.degrees(np.arctan2(vecs[1, 1], vecs[0, 1]))
    w, h = 2 * 2 * np.sqrt(vals[1]), 2 * 2 * np.sqrt(vals[0])
    ax.add_patch(Ellipse(mean, w, h, angle=angle, facecolor=color, alpha=fill_alpha, lw=0))
    ax.add_patch(Ellipse(mean, w, h, angle=angle, facecolor="none", edgecolor=color, lw=lw))


target = RANGE * SIGHT
cam_mean, cam_cov = target + 1.1 * SIGHT + 0.08 * ACROSS, covariance(1.6, 0.18)
rad_mean, rad_cov = target - 0.15 * SIGHT - 0.5 * ACROSS, covariance(0.2, 1.3)
cam_info, rad_info = np.linalg.inv(cam_cov), np.linalg.inv(rad_cov)
fused_cov = np.linalg.inv(cam_info + rad_info)
fused_mean = fused_cov @ (cam_info @ cam_mean + rad_info @ rad_mean)

setup_style()
fig, ax = plt.subplots(figsize=(5.2, 5.2), facecolor=SURFACE)
ax.set_facecolor(SURFACE)
ax.plot([0, 10.5 * SIGHT[0]], [0, 10.5 * SIGHT[1]], color=POINT, lw=1.2, ls=(0, (4, 3)))
ax.add_patch(Polygon([(-0.35, -0.5), (0.35, -0.5), (0, 0.3)], color=INK2, lw=0))

draw_ellipse(ax, cam_mean, cam_cov, MODEL, 0.15, 1.8)
draw_ellipse(ax, rad_mean, rad_cov, INK2, 0.1, 1.8)
draw_ellipse(ax, fused_mean, fused_cov, TRUTH, 0.7, 2.0)

ax.text(*(cam_mean + 3.6 * SIGHT + 0.5 * ACROSS), "camera", color=MODEL, fontsize=17,
        ha="left", va="center")
ax.text(*(rad_mean - 2.9 * ACROSS), "radar", color=INK2, fontsize=17, ha="right", va="center")
ax.text(*(fused_mean + 0.5 * ACROSS - 1.3 * SIGHT), "fused", color=TRUTH, fontsize=17,
        ha="left", va="center")

ax.set_aspect("equal")
ax.set_xlim(-3.5, 7.5)
ax.set_ylim(-0.8, 11)
ax.axis("off")

save(fig, __file__)
