"""Today's records predict today's rescues, but not next week's.

Run: python a-week-ahead.py  (requires numpy, scipy, matplotlib)
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.offsetbox import AnchoredOffsetbox, HPacker, TextArea
from matplotlib.patches import Polygon
from scipy.interpolate import PchipInterpolator

DAYS = 14
LAG = 7
# Set by hand so the week-earlier weather is unremarkable on hot days and the
# hottest day falls in the week both sales rows show.
DAILY_WEATHER = [0.1, 0.7, 0.3, -0.1, -0.6, 0.8, 0.3, -0.1, -0.2, -0.4, 1.0,
                 0.0, 0.1, -0.7, -0.2, 0.9, -0.1, -0.6, -0.2, 0.7, -0.1]
BUMP_WIDTH = 0.3  # days

BLUE = "#0284c7"
AMBER = "#d97706"
SLATE = "#64748b"
MUTED = "#94a3b8"
RIBBON = "#f1f5f9"

plt.rcParams.update(
    {
        "font.family": ["Helvetica Neue", "Helvetica", "Arial", "sans-serif"],
        "font.size": 12,
    }
)

n = DAYS + LAG
weather = np.array(DAILY_WEATHER)
crowd = np.exp(2.5 * weather)
rng = np.random.default_rng(640)
sales = crowd * np.exp(0.35 * rng.normal(size=n))
rescues = crowd * np.exp(0.35 * rng.normal(size=n))

# Each day spans one unit, so the two weeks meet at LAG - 0.5.
t = np.linspace(-0.5, DAYS - 0.5, 2000)


# A shared scale keeps the repeated week identical across the sales rows.
def bumps(daily, scale):
    return sum(v * np.exp(-0.5 * ((t - d) / BUMP_WIDTH) ** 2) for d, v in enumerate(daily)) / scale


def smooth(record, start):
    curve = PchipInterpolator(np.arange(n), record)(t + start)
    return (curve - record.min()) / np.ptp(record)


now, week_before = slice(LAG, n), slice(0, DAYS)
# The shifted rows draw their record from week 2 on, so the reader stays on the
# week being forecast instead of comparing two weeks at once.
rows = [
    (sales[now], bumps(sales[now], sales.max()), SLATE, "ice cream sales, same week", 0),
    (sales[week_before], bumps(sales[week_before], sales.max()), SLATE, "ice cream sales, a week earlier", LAG),
    (weather[week_before], smooth(weather, 0), AMBER, "weather, a week earlier", LAG),
]
target = bumps(rescues[now], rescues[now].max())

fig, axes = plt.subplots(3, 1, figsize=(8, 3.6), sharex=True, gridspec_kw={"hspace": 0.55})

for ax, (daily, curve, color, name, first) in zip(axes, rows):
    shown = t >= first - 0.5
    ax.plot(t, target, color=BLUE, lw=2.2)
    ax.plot(t[shown], curve[shown], color=color, lw=2.2)
    ax.set_axis_off()
    ax.set_xlim(t[0], t[-1])
    ax.set_ylim(-0.05, 1.05)

    title = HPacker(
        children=[
            TextArea("Beach rescues", textprops={"color": BLUE, "fontsize": 13}),
            TextArea("vs.", textprops={"color": MUTED, "fontsize": 13}),
            TextArea(name, textprops={"color": color, "fontsize": 13}),
        ],
        sep=5,
        pad=0,
    )
    ax.add_artist(
        AnchoredOffsetbox("lower left", child=title, pad=0, borderpad=0, frameon=False,
                          bbox_to_anchor=(0, 1.02), bbox_transform=ax.transAxes)
    )
    # Adding zero turns a rounded -0.0 into 0.0, so no sign appears that is not there.
    r = round(np.corrcoef(daily[first:], rescues[now][first:])[0, 1], 1) + 0.0
    ax.text(1, 1.02, f"correlation {r:.1f}", transform=ax.transAxes, ha="right", va="bottom",
            color=MUTED, fontsize=11)

bottom = axes[-1]
bottom.set_axis_on()
bottom.patch.set_visible(False)
for side in ("left", "right", "top"):
    bottom.spines[side].set_visible(False)
bottom.spines["bottom"].set(color=MUTED, position=("outward", 6))
bottom.set_yticks([])
bottom.set_xticks([-0.5, LAG - 0.5, DAYS - 0.5], labels=[])
bottom.set_xticks([(LAG - 1) / 2, LAG + (LAG - 1) / 2], labels=["week 1", "week 2"], minor=True)
bottom.tick_params(which="major", color=MUTED, length=4)
bottom.tick_params(which="minor", length=0, labelcolor=MUTED, labelsize=11)

# Links the first week of the top row to where it reappears below.
def corner(ax, x, top):
    return fig.transFigure.inverted().transform(ax.transData.transform((x, 1.05 if top else -0.05)))


edge = LAG - 0.5
ribbon = [
    corner(axes[0], t[0], True), corner(axes[0], edge, True), corner(axes[0], edge, False),
    corner(axes[1], t[-1], True), corner(axes[1], t[-1], False), corner(axes[1], edge, False),
    corner(axes[1], edge, True), corner(axes[0], t[0], False),
]
fig.add_artist(Polygon(ribbon, closed=True, facecolor=RIBBON, edgecolor="none", zorder=0))

fig.savefig(
    Path(__file__).with_name("a-week-ahead.png"),
    dpi=200,
    bbox_inches="tight",
    facecolor="white",
)
