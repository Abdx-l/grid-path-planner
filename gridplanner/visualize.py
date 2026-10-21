"""Optional Matplotlib rendering, imported only when requested."""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np


def canvas(grid):
    image = np.ones((grid.height, grid.width, 3), dtype=float)
    for x, y in grid.walls:
        image[y, x] = (0.15, 0.20, 0.27)
    return image


def plot_result(grid, result, output):
    image = canvas(grid)
    for x, y in result.expanded:
        image[y, x] = (0.69, 0.83, 0.96)
    for x, y in result.path:
        image[y, x] = (0.95, 0.35, 0.20)
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.imshow(image, interpolation="nearest")
    ax.set_title(f"Expanded {len(result.expanded)} cells; cost {result.cost:.2f}")
    ax.set_xticks([])
    ax.set_yticks([])
    fig.savefig(output, dpi=150, bbox_inches="tight")
    plt.close(fig)


def animate_result(grid, result, output):
    base = canvas(grid)
    fig, ax = plt.subplots(figsize=(7, 7))
    artist = ax.imshow(base, interpolation="nearest")
    ax.set_xticks([])
    ax.set_yticks([])
    stride = max(1, len(result.expanded) // 100)
    frames = list(range(0, len(result.expanded), stride)) + [len(result.expanded)]

    def draw(frame):
        image = base.copy()
        for x, y in result.expanded[:frame]:
            image[y, x] = (0.69, 0.83, 0.96)
        if frame < len(result.frontiers):
            for x, y in result.frontiers[frame]:
                image[y, x] = (0.98, 0.77, 0.32)
        if frame == len(result.expanded):
            for x, y in result.path:
                image[y, x] = (0.95, 0.35, 0.20)
        artist.set_data(image)
        return (artist,)

    animation = FuncAnimation(fig, draw, frames=frames, interval=80, blit=True)
    animation.save(output, writer=PillowWriter(fps=12))
    plt.close(fig)

