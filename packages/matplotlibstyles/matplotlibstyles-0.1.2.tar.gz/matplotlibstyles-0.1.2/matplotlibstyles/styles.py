"""Styles for creating plots with matplotlib."""

import matplotlib as mpl
from matplotlib import pyplot as plt

SHARE_PGF_PREAMBLE = "\n".join(
    [
        r"\usepackage[RGB]{xcolor}",
        r"\usepackage{fontspec}",
        r"\usepackage{unicode-math}",
        r"\setmainfont{STIX Two Text}",
        r"\setmathfont{STIX Two Math}",
        # r"\usepackage{stix2}",
        r"\usepackage{nicefrac}",
        r"\usepackage{siunitx}",
        r"\DeclareSIUnit{\molar}{M}",
        r"\DeclareSIUnit{\kb}{\ensuremath{\mathit{k_\textrm{B}}}}",
        r"\DeclareSIUnit{\kbT}{\ensuremath{\mathit{k_\textrm{B} T}}}",
    ]
)

TEXTBLACK = "0.125"


def set_default_style():

    # Lines
    plt.rcParams["lines.linewidth"] = 1.0
    plt.rcParams["lines.markeredgewidth"] = 1.0
    plt.rcParams["lines.markersize"] = 5

    # Fonts and symbols
    plt.rcParams["font.family"] = "serif"
    plt.rcParams["font.serif"] = "Times New Roman"
    plt.rcParams["font.weight"] = "normal"
    plt.rcParams["font.size"] = 8
    plt.rcParams["axes.titlesize"] = 8
    plt.rcParams["axes.labelsize"] = 8
    plt.rcParams["xtick.labelsize"] = 8
    plt.rcParams["ytick.labelsize"] = 8
    plt.rcParams["legend.fontsize"] = 8
    plt.rcParams["text.usetex"] = False
    plt.rcParams["mathtext.rm"] = "serif"
    plt.rcParams["mathtext.it"] = "serif:italic"
    plt.rcParams["mathtext.fontset"] = "stix"

    # Axes
    plt.rcParams["axes.linewidth"] = 0.8
    plt.rcParams["axes.spines.right"] = False
    plt.rcParams["axes.spines.top"] = False

    # Ticks
    plt.rcParams["xtick.color"] = (0.0, 0.0, 0.0)
    plt.rcParams["xtick.major.width"] = 0.8
    plt.rcParams["ytick.color"] = (0.0, 0.0, 0.0)
    plt.rcParams["ytick.major.width"] = 0.8

    # Errorbar plots
    plt.rcParams["errorbar.capsize"] = 2

    # Legend
    plt.rcParams["legend.frameon"] = False
    plt.rcParams["legend.framealpha"] = 0.0


def set_thin_style():

    # Lines
    plt.rcParams["lines.linewidth"] = 0.5
    plt.rcParams["lines.markeredgewidth"] = 0.7
    plt.rcParams["lines.markersize"] = 2.5

    # Fonts and symbols
    plt.rcParams["font.family"] = "serif"
    plt.rcParams["font.serif"] = "Times New Roman"
    plt.rcParams["font.weight"] = "normal"
    plt.rcParams["font.size"] = 8
    plt.rcParams["axes.titlesize"] = 8
    plt.rcParams["axes.labelsize"] = 8
    plt.rcParams["xtick.labelsize"] = 8
    plt.rcParams["ytick.labelsize"] = 8
    plt.rcParams["legend.fontsize"] = 8
    plt.rcParams["text.usetex"] = False
    plt.rcParams["mathtext.rm"] = "serif"
    plt.rcParams["mathtext.it"] = "serif:italic"
    plt.rcParams["mathtext.fontset"] = "stix"

    # Axes
    plt.rcParams["axes.edgecolor"] = (0.0, 0.0, 0.0)
    plt.rcParams["axes.linewidth"] = 0.5
    plt.rcParams["axes.spines.right"] = False
    plt.rcParams["axes.spines.top"] = False

    # Ticks
    plt.rcParams["xtick.color"] = (0.0, 0.0, 0.0)
    plt.rcParams["xtick.major.width"] = 0.5
    plt.rcParams["ytick.color"] = (0.0, 0.0, 0.0)
    plt.rcParams["ytick.major.width"] = 0.5

    # Errorbar plots
    plt.rcParams["errorbar.capsize"] = 1.0

    # Legend
    plt.rcParams["legend.frameon"] = False
    plt.rcParams["legend.framealpha"] = 0.0


def set_default_latex_style():
    mpl.use("pgf")

    plt.rcParams["lines.linewidth"] = 1.0
    plt.rcParams["lines.markeredgewidth"] = 1.0
    plt.rcParams["lines.markersize"] = 2.5

    # Fonts and symbols
    plt.rcParams["pgf.texsystem"] = "lualatex"
    plt.rcParams["pgf.rcfonts"] = False
    plt.rcParams["text.usetex"] = True
    plt.rcParams["font.family"] = "serif"
    plt.rcParams["font.serif"] = ["STIX Two Text"]
    plt.rcParams["text.color"] = "black"
    plt.rcParams["font.size"] = 8
    plt.rcParams["axes.titlesize"] = 8
    plt.rcParams["axes.labelsize"] = 8
    plt.rcParams["xtick.labelsize"] = 8
    plt.rcParams["ytick.labelsize"] = 8
    plt.rcParams["legend.fontsize"] = 8
    plt.rcParams["pgf.preamble"] = SHARED_PGF_PREAMBLE

    # Axes
    plt.rcParams["axes.edgecolor"] = "black"
    plt.rcParams["axes.labelcolor"] = "black"
    plt.rcParams["axes.linewidth"] = 0.8
    plt.rcParams["axes.spines.right"] = False
    plt.rcParams["axes.spines.top"] = False

    # Ticks
    plt.rcParams["xtick.color"] = "black"
    plt.rcParams["xtick.major.width"] = 0.8
    plt.rcParams["ytick.color"] = "black"
    plt.rcParams["ytick.major.width"] = 0.8

    # Errorbar plots
    plt.rcParams["errorbar.capsize"] = 2

    # Legend
    plt.rcParams["legend.frameon"] = False
    plt.rcParams["legend.framealpha"] = 0.0


def set_thin_latex_style():
    mpl.use("pgf")

    plt.rcParams["lines.linewidth"] = 0.5
    plt.rcParams["lines.markeredgewidth"] = 0.7
    plt.rcParams["lines.markersize"] = 2.5

    # Fonts and symbols
    plt.rcParams["pgf.texsystem"] = "lualatex"
    plt.rcParams["pgf.rcfonts"] = False
    plt.rcParams["text.usetex"] = True
    plt.rcParams["font.family"] = "serif"
    plt.rcParams["font.serif"] = ["STIX Two Text"]
    plt.rcParams["text.color"] = TEXTBLACK
    plt.rcParams["font.size"] = 8
    plt.rcParams["axes.titlesize"] = 8
    plt.rcParams["axes.labelsize"] = 8
    plt.rcParams["xtick.labelsize"] = 8
    plt.rcParams["ytick.labelsize"] = 8
    plt.rcParams["legend.fontsize"] = 8
    plt.rcParams["pgf.preamble"] = SHARE_PGF_PREAMBLE

    # Axes
    plt.rcParams["axes.edgecolor"] = TEXTBLACK
    plt.rcParams["axes.labelcolor"] = TEXTBLACK
    plt.rcParams["axes.linewidth"] = 0.5
    plt.rcParams["axes.spines.right"] = False
    plt.rcParams["axes.spines.top"] = False

    # Ticks
    plt.rcParams["xtick.color"] = TEXTBLACK
    plt.rcParams["xtick.major.width"] = 0.5
    plt.rcParams["ytick.color"] = TEXTBLACK
    plt.rcParams["ytick.major.width"] = 0.5

    # Errorbar plots
    plt.rcParams["errorbar.capsize"] = 1.0

    # Legend
    plt.rcParams["legend.frameon"] = False
    plt.rcParams["legend.framealpha"] = 0.0
