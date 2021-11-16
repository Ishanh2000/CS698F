import numpy as np
import matplotlib.pyplot as plt

DATA_DIR = "raw_data/"


def plot_acc_data(filename, show_plot=False):
    timestamps = []
    acc_total = []
    acc_x = []
    acc_y = []
    acc_z = []
    with open(DATA_DIR + filename, "r") as f:
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


# plot_acc_data("fwd_bkwd.csv", show_plot=True)
# plot_acc_data("wave.csv", show_plot=True)
plot_acc_data("cross.csv", show_plot=True)
plt.show()
