import numpy as np
import matplotlib.pylab as plt
from .bipolar import bipolar
from matplotlib.colors import LinearSegmentedColormap

# get colormap
ncolors = 256
color_array = plt.get_cmap('jet')(range(ncolors))

# change alpha values
color_array[:,-1] = np.linspace(0.0, 1.0,ncolors)

# create a colormap object
map_object = LinearSegmentedColormap.from_list(name='jet_alpha',colors=color_array)

# register this new colormap with matplotlib
plt.register_cmap(cmap=map_object)

plt.rcParams['font.size'] = 12
plt.rcParams['axes.labelsize'] = 10
plt.rcParams['axes.titlesize'] = 10
plt.rcParams['xtick.labelsize'] = 8
plt.rcParams['ytick.labelsize'] = 8
plt.rcParams['legend.fontsize'] = 12
plt.rcParams['figure.titlesize'] = 14


def show(data, epsr, sources, intensity=False, theme='bright', label=None, saveas=''):
    fig, ax = plt.subplots(1, 1, figsize=(4, 4), dpi=100)

    if theme == 'dark':
        colors = 'magma' if intensity else bipolar(neutral=0.0)
        outline = 'white'
        source_color = 'lightyellow'
    else:
        colors = 'jet_alpha' if intensity else 'RdBu'
        outline = 'gray'
        source_color = 'gray'

    ax.imshow(data.T, cmap=colors)
    ax.contour(epsr.T, colors=outline, alpha=0.1)

    for src in sources:
        ax.plot(src[0], src[1], color=source_color)

    ax.invert_yaxis()

    if label:
        offset = int(data.shape[0] / 12)
        ax.text(offset, data.shape[1]-1.5*offset, label, color=outline)

    ax.axis('off')
#     ax.add_artist(ScaleBar(resolution))
    plt.tight_layout()
    if saveas:
        plt.savefig(saveas)
        plt.close(fig)
    else:
        plt.show()


def show_design(epsr, *sources):
    fig, ax = plt.subplots(1, 1, dpi=100)

    ax.imshow(epsr.T, cmap='Blues_r')
    for src in sources:
        ax.plot(src[0], src[1], color="red")

    ax.invert_yaxis()

    # Get nice a nice grid going
    ax.minorticks_on()
    ax.grid(which='both', color='white', linestyle='-')
    ax.grid(which='minor', linestyle=':', linewidth='0.5', color='lightgray')

    # Also show tics on top and right
    ax.xaxis.set_ticks_position('both')
    ax.yaxis.set_ticks_position('both')

    ax.set_xlabel("px")
    ax.set_ylabel("px")

    plt.show()


""" Utilities for plotting and visualization """

def real(val, outline=None, ax=None, cbar=False, cmap='RdBu', outline_alpha=0.5):
    """Plots the real part of 'val', optionally overlaying an outline of 'outline'
    """

    if ax is None:
        fig, ax = plt.subplots(1, 1, constrained_layout=True)

    vmax = np.abs(val).max()
    h = ax.imshow(np.real(val.T), cmap=cmap, origin='lower', vmin=-vmax, vmax=vmax)

    if outline is not None:
        ax.contour(outline.T, 0, colors='k', alpha=outline_alpha)

    ax.set_ylabel('y')
    ax.set_xlabel('x')
    if cbar:
        plt.colorbar(h, ax=ax)

    return ax

def abs(val, outline=None, ax=None, cbar=False, cmap='magma', outline_alpha=0.5, outline_val=None):
    """Plots the absolute value of 'val', optionally overlaying an outline of 'outline'
    """

    if ax is None:
        fig, ax = plt.subplots(1, 1, constrained_layout=True)

    vmax = np.abs(val).max()
    h = ax.imshow(np.abs(val.T), cmap=cmap, origin='lower', vmin=0, vmax=vmax)

    if outline_val is None and outline is not None: outline_val = 0.5*(outline.min()+outline.max())
    if outline is not None:
        ax.contour(outline.T, [outline_val], colors='w', alpha=outline_alpha)

    ax.set_ylabel('y')
    ax.set_xlabel('x')
    if cbar:
        plt.colorbar(h, ax=ax)

    return ax
