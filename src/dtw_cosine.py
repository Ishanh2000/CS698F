import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import NullFormatter, FormatStrFormatter


def norm(x):
    return np.sqrt(x[0] * x[0] + x[1] * x[1] + x[2] * x[2])


def metric(ta, tb):
    dx = ta[0] - tb[0]
    dy = ta[1] - tb[1]
    dz = ta[2] - tb[2]
    dirn = (ta[0] * tb[0] + ta[1] * tb[1] + ta[2] * tb[2]) / (norm(ta) * norm(tb) + 1e-6)
    return (1 - 0.5 * dirn) * norm([dx, dy, dz])


def dtw(template, data):
    M, N = len(template[0]), len(data[0])

    # Initialization
    cost = [[None for j in range(N + 1)] for i in range(M + 1)]
    for i in range(1, M + 1):
        cost[i][0] = [float("inf"), ((i - 1), 0)]  # [cost, parent]
    for j in range(1, N + 1):
        cost[0][j] = [float("inf"), (0, (j - 1))]  # [cost, parent]
    cost[0][0] = [0, None]

    # Algorithm
    for i in range(1, M + 1):
        for j in range(1, N + 1):
            dist = metric([a[i - 1] for a in template], [a[j - 1] for a in data])
            add, parent = cost[i - 1][j][0], ((i - 1), j)
            if add > cost[i - 1][j - 1][0]:
                add, parent = cost[i - 1][j - 1][0], ((i - 1), (j - 1))
            if add > cost[i][j - 1][0]:
                add, parent = cost[i][j - 1][0], (i, (j - 1))
            cost[i][j] = [(dist / N + add), parent]

    totalCost = cost[M][N][0]

    alignment = [(M, N)]
    while True:
        i, j = alignment[-1]
        parent = cost[i][j][1]
        if parent == None:
            break
        alignment.append(parent)
    alignment.reverse()
    costs = [[0 for j in range(N + 1)] for i in range(M + 1)]
    for i in range(M + 1):
        for j in range(N + 1):
            costs[i][j] = cost[i][j][0]
    alignment = [(a[0] - 1, a[1] - 1) for a in alignment[1:]]

    return totalCost, costs, alignment


def plot_alignment(cost, alignment, data_x, data_y):
    dtw_plot = plt.figure(1)
    cost = np.array(cost)

    plt.imshow(cost.T, origin="lower", cmap=cm.cool, interpolation="nearest", aspect="auto")
    plt.colorbar()
    plt.plot([x[0] for x in alignment], [x[1] for x in alignment], "b")

    plt.ylim((-0.5, cost.shape[1] - 0.5))
    plt.xlim((-0.5, cost.shape[0] - 0.5))

    return dtw_plot
