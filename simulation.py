import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from matplotlib.colors import ListedColormap, BoundaryNorm
from gol import GameOfLife, DormantLife

if __name__ == "__main__":
    init_grid = np.random.choice([0, 1], p=[0.80, 0.20], size=[30, 30])
    # init_grid = np.array([
    #     [0, 0, 0],
    #     [1, 1, 0],
    #     [1, 1, 0]
    # ])
    gol = GameOfLife(init_grid)
    dl = DormantLife(init_grid)
    colors = ["white", "tab:blue", "lightblue"]
    bounds = [-0.5, 0.5, 1.5, 2.5]
    cmap = ListedColormap(colors)
    norm = BoundaryNorm(bounds, cmap.N, clip=True)
    fig, ax = plt.subplots(figsize=(8, 3), ncols=2)
    ax[0].set(title=r"Game of Life: $N_\text{alive} = %d$"%gol.alive_count)
    ax[1].set(title=r"Dormant Life: $N_\text{alive} = %d$"%dl.alive_count)
    mat_gol = ax[0].matshow(gol.grid, cmap=cmap, norm=norm)
    mat_dl = ax[1].matshow(dl.grid, cmap=cmap, norm=norm)
    def update(frame):
        mat_gol.set_data(gol.step())
        mat_dl.set_data(dl.step(alpha=0.1))
        ax[0].set(title=r"Game of Life: $N_\text{alive} = %d$"%gol.alive_count)
        ax[1].set(title=r"Dormant Life: $N_\text{alive} = %d$"%dl.alive_count)
    ani = animation.FuncAnimation(fig, update, interval=1, save_count=100)
    plt.show()