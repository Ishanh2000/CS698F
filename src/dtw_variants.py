import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import NullFormatter, FormatStrFormatter
from fastdtw import fastdtw


def norm(x):
    return np.sqrt(x[0] * x[0] + x[1] * x[1] + x[2] * x[2])


def metric(ta, tb):
    dx = ta[0] - tb[0]
    dy = ta[1] - tb[1]
    dz = ta[2] - tb[2]
    dirn = (ta[0] * tb[0] + ta[1] * tb[1] + ta[2] * tb[2]) / (norm(ta) * norm(tb) + 1e-6)
    return (1 - 0.5 * dirn) * norm([dx, dy, dz])


def dtw_sakoe_chiba(template, data):
    M, N = len(template[0]), len(data[0])
    W = int(M / 8) + int(abs(N - M) / 2)
    # Initialization
    cost = [[[int(1e8), None] for j in range(N + 1)] for i in range(M + 1)]
    for i in range(1, M + 1):
        cost[i][0] = [float("inf"), ((i - 1), 0)]  # [cost, parent]
    for j in range(1, N + 1):
        cost[0][j] = [float("inf"), (0, (j - 1))]  # [cost, parent]
    cost[0][0] = [0, None]
    # Algorithm
    for i in range(1, M + 1):
        for j in range(1, N + 1):
            if abs((j - N * i / M)) > W:
                continue
            dist = metric([a[i - 1] for a in template], [a[j - 1] for a in data])
            # print(cost[i - 1][j], i - 1, j)
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


def dtw_itakura(template, data):
    M, N = len(template[0]), len(data[0])
    m = np.arctan(N / M)
    d = 0.39

    def in_itakura(i, j):
        x = i - 1
        y = j - 1
        inside = False
        a1 = np.arctan(j / i) if i > 0 else m
        a2 = np.arctan((j - N) / (i - M)) if i != M else m
        if abs(a1 - m) < d and abs(a2 - m) < d:
            inside = True
        return inside

    # Initialization
    cost = [[[int(1e8), None] for j in range(N + 1)] for i in range(M + 1)]
    for i in range(1, M + 1):
        cost[i][0] = [float("inf"), ((i - 1), 0)]  # [cost, parent]
    for j in range(1, N + 1):
        cost[0][j] = [float("inf"), (0, (j - 1))]  # [cost, parent]
    cost[0][0] = [0, None]
    # Algorithm
    for i in range(1, M + 1):
        for j in range(1, N + 1):
            if not in_itakura(i, j):
                continue
            dist = metric([a[i - 1] for a in template], [a[j - 1] for a in data])
            # print(cost[i - 1][j], i - 1, j)
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
    alignment = [(a[0] - 1, a[1] - 1) for a in alignment[:]]

    return totalCost, costs, alignment


def fast_dtw(template, data):
    M, N = len(template), len(data)
    x = np.array([[template[0][i], template[1][i], template[2][i]] for i in range(len(template[0]))])
    y = np.array([[data[0][i], data[1][i], data[2][i]] for i in range(len(data[0]))])
    totalCost, alignment = fastdtw(x, y, dist=metric)
    cost_matrix = np.zeros((M + 1, N + 1))
    return totalCost, cost_matrix, alignment


def plot_alignment_with_variants(cost, alignment, data_x, data_y, itakura=False, sakoe_chiba=False, fig=1):
    dtw_plot = plt.figure(fig)
    cost = np.array(cost, dtype="float")
    cost[cost == int(1e8)] = None

    M, N = alignment[-1]

    plt.imshow(
        cost.T,
        origin="lower",
        cmap=cm.cool,
        interpolation="nearest",
        aspect="auto",
    )
    plt.colorbar()
    plt.plot([x[0] for x in alignment], [x[1] for x in alignment], "b")

    if sakoe_chiba:
        T0 = int(M / 8) + int(abs(M - N) / 2)
        plt.plot(range(M + 1), [x * N / M + T0 for x in range(M + 1)], "r")
        plt.plot(range(M + 1), [x * N / M - T0 for x in range(M + 1)], "r")

    if itakura:
        m = np.arctan(N / M)
        d = 0.39
        s1 = np.tan(d + m)
        s2 = np.tan(d - m)
        x1 = int((N - s2 * M) / (s1 - s2))
        x2 = int((N - s1 * M) / (s2 - s1))
        plt.plot(range(x1), [int(s1 * x) for x in range(x1)], "r")
        # plt.plot(range(x2), [int(s2 * x) for x in range(x2)], "r")
        plt.plot(range(x1, M + 1), [int(N + s1 * (x - M)) for x in range(x1, M + 1)], "g")
        # plt.plot(range(x2, M + 1), [int(N + s2 * (x - M)) for x in range(x2, M + 1)], "g")

    plt.ylim((-0.5, cost.shape[1] - 0.5))
    plt.xlim((-0.5, cost.shape[0] - 0.5))

    return dtw_plot
