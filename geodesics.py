from geoopt import Stereographic
import torch
import numpy as np
import matplotlib.pyplot as plt
import math
import seaborn as sns
from matplotlib import rcParams
sns.set_style("white")

def add_geodesic_grid(ax: plt.Axes, manifold: Stereographic, line_width=0.1):

    # define geodesic grid parameters
    N_EVALS_PER_GEODESIC = 10000
    STYLE = "-"
    COLOR = "salmon"
    LINE_WIDTH = line_width

    # get manifold properties
    K = manifold.k.item()
    R = manifold.radius.item()

    if K < 0:
        r = torch.tensor((R, 0.0), dtype=manifold.dtype)
        r = manifold.projx(r)
        max_dist_0 = manifold.dist0(r).item()
    else:
        max_dist_0 = math.pi * R
    circumference = 2*math.pi*R

    n_geodesics_per_circumference = 4 * 6  # multiple of 4!
    n_geodesics_per_quadrant = n_geodesics_per_circumference // 2
    grid_interval_size = circumference / n_geodesics_per_circumference
    if K < 0:
        n_geodesics_per_quadrant = int(max_dist_0 / grid_interval_size)

    # create time evaluation array for geodesics
    if K < 0:
        min_t = -1.2*max_dist_0
    else:
        min_t = -circumference/2.0
    t = torch.linspace(min_t, -min_t, N_EVALS_PER_GEODESIC)[:, None]

    def plot_geodesic(gv):
        ax.plot(*gv.t().numpy(), STYLE, color=COLOR, linewidth=LINE_WIDTH)

    u_x = torch.tensor((0.0, 1.0))
    u_y = torch.tensor((1.0, 0.0))

    o = torch.tensor((0.0, 0.0))
    if K < 0:
        x_geodesic = manifold.geodesic_unit(t, o, u_x)
        y_geodesic = manifold.geodesic_unit(t, o, u_y)
        plot_geodesic(x_geodesic)
        plot_geodesic(y_geodesic)
    else:
        # add the crosshair manually for the sproj of sphere
        # because the lines tend to get thicker if plotted
        # as done for K<0
        ax.axvline(0, linestyle=STYLE, color=COLOR, linewidth=LINE_WIDTH)
        ax.axhline(0, linestyle=STYLE, color=COLOR, linewidth=LINE_WIDTH)

    for i in range(1, n_geodesics_per_quadrant):
        i = torch.as_tensor(float(i))
        x = manifold.geodesic_unit(i*grid_interval_size, o, u_y)
        y = manifold.geodesic_unit(i*grid_interval_size, o, u_x)

        x_geodesic = manifold.geodesic_unit(t, x, u_x)
        y_geodesic = manifold.geodesic_unit(t, y, u_y)

        plot_geodesic(x_geodesic)
        plot_geodesic(y_geodesic)
        if K < 0:
            plot_geodesic(-x_geodesic)
            plot_geodesic(-y_geodesic)

lim = 1.1
coords = np.linspace(-lim, lim, 100)
xx, yy = np.meshgrid(coords, coords)
dist2 = xx ** 2 + yy ** 2
mask = dist2 <= 1
grid = np.stack([xx, yy], axis=-1)

manifold = Stereographic(-1)

dists = manifold.dist(torch.from_numpy(grid).float(), x)
dists[(~mask).nonzero()] = np.nan

fig, ax = plt.subplots(1, 1, figsize=(5, 5))
circle = plt.Circle((0, 0), 1, fill=False, color="black")

ax.add_artist(circle)
ax.set_xlim(-lim, lim)
ax.set_ylim(-lim, lim)
ax.set_aspect("equal")
add_geodesic_grid(ax, manifold, 1)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.xaxis.set_ticklabels([])
ax.yaxis.set_ticklabels([])

plt.show()
