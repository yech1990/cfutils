#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2019 yech <yech1990@gmail.com>
#
# Distributed under terms of the MIT license.

"""Chromatogram File Utils.

show alignment with matplotlib

author:     Fabio Zanini
date:       09/12/13
content:    Plot functions for Sanger chromatographs.
modified:   By Ye Chang in 2018-05-14
"""

from collections import defaultdict
from typing import Tuple

import matplotlib as mpl
import matplotlib.pyplot as plt
from Bio.SeqRecord import SeqRecord

from .align import SitePair
from .utils import get_logger

LOGGER = get_logger(__name__)


def plot_chromatograph(
    seq: SeqRecord, region: Tuple[int, int] = None, ax: mpl.axes = None
) -> plt.axes:
    """Plot Sanger chromatograph.

    region: include both start and end (1-based)
    """
    if seq is None:
        return ax

    if region is None:
        # turn into 0 based for better indexing
        region_start, region_end = 0, len(seq)
    else:
        region_start = max(region[0], 0)
        region_end = min(region[1], len(seq))

    if ax is None:
        _, ax = plt.subplots(1, 1, figsize=(16, 6))

    _colors = defaultdict(
        lambda: "purple", {"A": "g", "C": "b", "G": "k", "T": "r"}
    )

    # Get signals
    peaks = seq.annotations["peak positions"]
    trace_x = seq.annotations["trace_x"]
    traces_y = [seq.annotations["channel " + str(i)] for i in range(1, 5)]
    bases = seq.annotations["channels"]

    xlim_left, xlim_right = peaks[region_start] - 0.5, peaks[region_end] + 0.5

    # subset peak and sequence
    peak_zip = [
        (p, s) for p, s in zip(peaks, seq) if region_start <= p <= region_end
    ]
    peaks, seq = list(zip(*peak_zip))

    # subset trace_x and traces_y together
    trace_zip = [
        (x, *ys)
        for x, *ys in zip(trace_x, *traces_y)
        if xlim_left <= x <= xlim_right
    ]
    if not trace_zip:
        return ax
    trace_x, *traces_y = list(zip(*trace_zip))

    # Plot traces
    trmax = max(map(max, traces_y))
    for base in bases:
        trace_y = [1.0 * ci / trmax for ci in traces_y[bases.index(base)]]
        ax.plot(trace_x, trace_y, color=_colors[base], lw=2, label=base)
        ax.fill_between(
            trace_x, 0, trace_y, facecolor=_colors[base], alpha=0.125
        )

    # Plot bases at peak positions
    for i, peak in enumerate(peaks):
        #  LOGGER.debug(f"{i}, {peak}, {seq[i]}, {xlim_left + i}")
        ax.text(peak, -0.11, seq[i], color=_colors[seq[i]], va="center")

    ax.set_ylim(bottom=-0.15, top=1.05)
    #  peaks[0] - max(2, 0.02 * (peaks[-1] - peaks[0])),
    #  right=peaks[-1] + max(2, 0.02 * (peaks[-1] - peaks[0])),
    ax.set_xlim(xlim_left, xlim_right)
    ax.set_xticks(peaks)
    ax.set_xticklabels(list(range(region_start + 1, region_end + 1)))
    # hide y axis
    ax.set_yticklabels([])
    ax.get_yaxis().set_visible(False)
    # hide border
    ax.spines["left"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    # hide grid
    ax.grid(False)
    # set legend
    ax.legend(loc="upper left", bbox_to_anchor=(0.95, 0.99))
    return ax


def highlight_base(
    pos_highlight: int, seq: SeqRecord, ax: mpl.axes, passed_filter=True
) -> mpl.axes:
    """Highlight the area around a peak with a rectangle."""

    peaks = seq.annotations["peak positions"]
    peak = peaks[pos_highlight - 1]

    xmin, xmax = ax.get_xlim()
    if not xmin <= peak < xmax:
        raise ValueError("peak not within plot bounds")

    if pos_highlight == 1:
        xmin = -0.5
    else:
        xmin = 0.5 * (peaks[pos_highlight - 1] + peaks[pos_highlight - 2])

    if pos_highlight == len(peaks):
        xmax = -0.5
    else:
        xmax = 0.5 * (peaks[pos_highlight - 1] + peaks[pos_highlight])
    ymin, ymax = ax.get_ylim()

    if passed_filter:
        fcolor = "yellow"
    else:
        fcolor = "grey"
    rec = mpl.patches.Rectangle(
        (xmin, ymin),
        (xmax - xmin),
        (ymax - ymin),
        edgecolor="none",
        facecolor=fcolor,
        alpha=0.3,
    )
    ax.add_patch(rec)
    return ax


def annotate_mutation(mut: SitePair, seq: SeqRecord, ax) -> mpl.axes:
    """Annotate mutation pattern chromatograph position."""
    peaks = seq.annotations["peak positions"]
    peak = peaks[mut.cf_pos - 1]
    ax.text(
        peak,
        0.99,
        f"{mut.ref_base}{mut.ref_pos}{mut.cf_base}",
        color="c",
        fontsize="large",
        fontweight="bold",
        rotation=45,
        ha="center",
        va="center",
    )
    return ax
