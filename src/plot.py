# AUM SHREEGANESHAAYA NAMAH|| AUM SHREEHANUMATE NAMAH||
import numpy as np
import matplotlib.pyplot as plt
import csv
import os

DATA_DIR = "raw_data/"


def plot_acc_data(filename, dir=DATA_DIR, show_plot=False):
    timestamps = []
    acc_total = []
    acc_x = []
    acc_y = []
    acc_z = []
    with open(dir + filename, "r") as f:
        for line in f.readlines()[1:]:
            ts, ax, ay, az, at = list(map(float, line.split(",")))
            timestamps.append(ts)
            acc_total.append(at)
            acc_x.append(ax)
            acc_y.append(ay)
            acc_z.append(az)
    total_plot = None
    axes_plot = None
    if show_plot:
        total_plot = plt.figure()
        plt.plot(timestamps, acc_total)
        plt.ylabel(r"Total Acceleration")
        plt.xlabel("Time (s)")
        # plt.locator_params(axis="x", nbins=40)
        axes_plot = plt.figure()
        plt.subplot(311)
        plt.plot(timestamps, acc_x)
        plt.ylabel(r"$a_x$")
        plt.xlabel("Time (s)")
        plt.subplot(312)
        plt.plot(timestamps, acc_y)
        plt.ylabel(r"$a_y$")
        plt.xlabel("Time (s)")
        plt.subplot(313)
        plt.plot(timestamps, acc_z)
        plt.ylabel(r"$a_z$")
        plt.xlabel("Time (s)")

    return timestamps, acc_total, (acc_x, acc_y, acc_z), (total_plot, axes_plot)


def plot_all_data(fname):
    f = open(fname)
    allRows = list(csv.reader(f))
    headers, rows = allRows[0], np.array([[float(x) for x in row] for row in allRows[1:]])
    dims = len(headers) - 1  # total dimensions of movements
    plt.figure()
    zeroLine = [0 for row in rows]
    for i in range(dims):
        # if i != 4: continue
        plt.subplot(2, 3, i + 1)
        plt.plot(rows[:, (i + 1)])
        plt.plot(zeroLine)
        plt.ylabel(headers[i + 1])
    plt.show()
    f.close()


def split_data(name, arr):
    f = open(f"../raw_data/{name}.csv")
    allRows = f.readlines()
    headers, rows = allRows[0], allRows[1:]
    for i in range(len(arr) - 1):
        if not os.path.isdir(f"../raw_templates/{name}"):
            os.mkdir(f"../raw_templates/{name}")
        fout = open(f"../raw_templates/{name}/{i+1}.csv", "w")
        fout.write(headers)
        for j in range(arr[i], arr[i + 1] + 1):
            fout.write(rows[j])  # now write data points
        fout.close()
    f.close()


if __name__ == "__main__":
    # plots originally done by Ashwin
    # plot_acc_data("fwd_bkwd.csv", show_plot=True)
    # plot_acc_data("wave.csv", show_plot=True)
    # plot_acc_data("cross.csv", show_plot=True)
    # plt.show()

    # additions by Ishanh
    plot_all_data(f"../raw_data/flip_flop.csv")
    # split_data("flip_flop", [
    #       53,  200,  337,  473,  602,  729,  875,  997, 1116, 1243, 1373, 1511, 1651, 1786, 1920, 2040, 2175,
    #     2311, 2443, 2570, 2715, 2834, 2979, 3091, 3226, 3353, 3489, 3613, 3735, 3882, 4024, 4141, 4277
    # ])
    for i in range(16):
        plot_all_data(f"../raw_templates/flip/{1+i}.csv")
    for i in range(16):
        plot_all_data(f"../raw_templates/flop/{1+i}.csv")

    #


# with intervals, 15 copies each of up_down, flip_flop, bow, left_right
