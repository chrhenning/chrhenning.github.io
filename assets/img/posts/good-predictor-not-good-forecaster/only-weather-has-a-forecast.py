"""Rescues and ice cream sales both follow the weather, but only the weather
has a forecast.

Run: python only-weather-has-a-forecast.py  (requires numpy, scipy, matplotlib)
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch
from scipy.interpolate import PchipInterpolator
from scipy.stats import norm

T_PAST = 3.0  # days
T_FUTURE = 2.0
SKILL_DAYS = 1.5
CLIM_SD = 0.7  # keeps the forecast within the range of measured weather
LEVELS = (0.5, 0.8)
# Set by hand so the link to rescues is easy to read: hot, cold, mild, then
# the two forecast days.
DAILY_WEATHER = [1.0, -1.0, 0.2, 0.8, -0.6]
PEAK = 15 / 24  # days

AMBER = "#d97706"
BLUE = "#0284c7"
SLATE = "#64748b"
INK = "#334155"
MUTED = "#94a3b8"
FAINT = "#cbd5e1"

plt.rcParams.update(
    {
        "font.family": ["Helvetica Neue", "Helvetica", "Arial", "sans-serif"],
        "font.size": 12,
    }
)

t = np.linspace(0, T_PAST + T_FUTURE, 4000)
past, fut = t <= T_PAST, t >= T_PAST
hour = (t % 1) * 24


def open_hours(start, end):
    x = np.clip((hour - start) / (end - start), 0, 1)
    return np.sin(np.pi * x) ** 1.5


# PCHIP, unlike a cubic spline, keeps the weather's extremes on the knots.
knots = np.arange(-1, len(DAILY_WEATHER) + 1) + PEAK
daily = np.array([0.0, *DAILY_WEATHER, 0.0])
weather_at = PchipInterpolator(knots, daily)
weather = weather_at(t)


def fade(x):
    return np.exp(-((np.clip(x - T_PAST, 0, None) / SKILL_DAYS) ** 2))


# Different opening hours keep rescues and sales from being trivially identical.
def rescues(w):
    return open_hours(11, 19) * np.exp(0.9 * w)


ice_cream = open_hours(9, 21) * np.exp(0.9 * weather)

# Forecast skill fades with lead time. Rescues are monotone in the weather, so
# weather quantiles map directly to rescue quantiles.
# Fading the daily values rather than the curve keeps forecast peaks at PEAK.
skill = fade(t)
i = np.searchsorted(knots, T_PAST)
fc_mean = PchipInterpolator(
    np.insert(knots, i, T_PAST), np.insert(fade(knots) * daily, i, weather_at(T_PAST))
)(t)
fc_sd = CLIM_SD * np.sqrt(1 - skill**2)

fig, (ax_w, ax_r, ax_i) = plt.subplots(
    3, 1, figsize=(8, 4.0), sharex=True, gridspec_kw={"hspace": 0.45}
)


def draw(ax, observed, color, name, forecast=None):
    if forecast is not None:
        for level in LEVELS:
            z = norm.ppf(0.5 + level / 2)
            ax.fill_between(
                t[fut],
                forecast(fc_mean - z * fc_sd)[fut],
                forecast(fc_mean + z * fc_sd)[fut],
                color=color,
                alpha=0.13,
                lw=0,
            )
        ax.plot(t[fut], forecast(fc_mean)[fut], color=color, lw=1.8, ls=(0, (2, 2)))
    ax.plot(t[past], observed[past], color=color, lw=2.2)
    ax.axvline(T_PAST, color=FAINT, lw=1, zorder=0)
    ax.set_axis_off()
    ax.set_xlim(0, t[-1])
    ax.text(0, 1.04, name, transform=ax.transAxes, color=color, fontsize=13)


draw(ax_w, weather, AMBER, "Weather", lambda w: w)
draw(ax_r, rescues(weather), BLUE, "Beach rescues", rescues)
draw(ax_i, ice_cream, SLATE, "Ice cream sales")

top = ax_w.get_xaxis_transform()
ax_w.text(T_PAST - 0.08, 1.04, "measured", transform=top, ha="right", color=INK, fontsize=11)
ax_w.text(T_PAST + 0.08, 1.04, "forecast", transform=top, ha="left", color=INK, fontsize=11)
ax_i.text(T_PAST + T_FUTURE / 2, 0.45, "no forecast", transform=ax_i.get_xaxis_transform(),
          ha="center", va="center", color=MUTED, fontsize=11)


def arrow(day, ax_from, ax_to, label, side):
    x = fig.transFigure.inverted().transform(ax_w.transData.transform((day, 0)))[0]
    down = ax_from.get_position().y0 > ax_to.get_position().y0
    upper, lower = (ax_from, ax_to) if down else (ax_to, ax_from)
    pad = 0.04 / fig.get_figheight()  # inches
    y_hi = upper.get_position().y0 - pad
    y_lo = lower.get_position().y1 + pad
    start, end = (y_hi, y_lo) if down else (y_lo, y_hi)
    fig.add_artist(
        FancyArrowPatch(
            (x, start),
            (x, end),
            transform=fig.transFigure,
            arrowstyle="-|>",
            mutation_scale=11,
            color=MUTED,
            lw=1.1,
        )
    )
    dx, ha = (0.012, "left") if side == "right" else (-0.012, "right")
    fig.text(x + dx, (start + end) / 2, label, ha=ha, va="center", color=MUTED, fontsize=11)


arrow(2 + PEAK, ax_i, ax_r, "only correlates", "left")
arrow(T_PAST + PEAK, ax_w, ax_r, "causes", "right")

fig.savefig(
    Path(__file__).with_name("only-weather-has-a-forecast.png"),
    dpi=200,
    bbox_inches="tight",
    facecolor="white",
)
