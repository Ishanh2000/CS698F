import numpy as np
import matplotlib.pyplot as plt
import os
import scipy.signal as sg
from scipy.signal import butter, lfilter, freqz
from timeit import default_timer as timer
import pywt

TEMPLATE_DIR = "raw_templates/"
PROC_DIR = "clean_templates/"
acc_gestures = ["wave", "cross", "forward", "backward"]
acc_gyro_gestures = ["flip", "flop"]

sample_rate = 100


def plot_compare(ts1, axes1, ts2, axess2):
    fig, ax = plt.subplots(2, 3)
    ax[0, 0].plot(ts1, axes1[0])
    ax[0, 0].set_ylabel(r"$a_x$")
    ax[0, 0].set_xlabel("Time (s)")
    ax[0, 1].plot(ts1, axes1[1])
    ax[0, 1].set_ylabel(r"$a_y$")
    ax[0, 1].set_xlabel("Time (s)")
    ax[0, 1].set_title("raw")
    ax[0, 2].plot(ts1, axes1[2])
    ax[0, 2].set_ylabel(r"$a_z$")
    ax[0, 2].set_xlabel("Time (s)")
    for axes2 in axess2:
        ax[1, 0].plot(ts2, axes2[0])
        ax[1, 0].set_ylabel(r"$a_x$")
        ax[1, 0].set_xlabel("Time (s)")
        ax[1, 1].plot(ts2, axes2[1])
        ax[1, 1].set_ylabel(r"$a_y$")
        ax[1, 1].set_xlabel("Time (s)")
        ax[1, 1].set_title("pre")
        ax[1, 2].plot(ts2, axes2[2])
        ax[1, 2].set_ylabel(r"$a_z$")
        ax[1, 2].set_xlabel("Time (s)")
    return fig


def read_acc_data(filename, show_plot=False):
    timestamps = []
    acc_total = []
    acc_x = []
    acc_y = []
    acc_z = []
    with open(filename, "r") as f:
        for line in f.readlines()[1:]:
            ts, ax, ay, az, at = list(map(float, line.split(",")))[:5]
            timestamps.append(ts)
            acc_total.append(at)
            acc_x.append(ax)
            acc_y.append(ay)
            acc_z.append(az)
    total_plot = None
    if show_plot:
        total_plot = plt.figure(0)
        plt.plot(timestamps, acc_total)
        plt.ylabel(r"Total Acceleration")
        plt.xlabel("Time (s)")
    return timestamps, acc_total, [acc_x, acc_y, acc_z], total_plot


def write_acc_data(ts, acc_axes, at, filename):
    with open(filename, "w+") as f:
        f.write("time,ax,ay,az,atotal")
        for t in range(len(ts)):
            f.write(
                ",".join([str(ts[t]), str(acc_axes[0][t]), str(acc_axes[1][t]), str(acc_axes[2][t]), str(at[t])]) + "\n"
            )


def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype="low", analog=False)
    return b, a


def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y


def wavelet_denoise(acc):
    w = pywt.Wavelet("sym4")
    maxlev = pywt.dwt_max_level(len(acc), w.dec_len)
    thresh = 0.05
    coeffs = pywt.wavedec(acc, "sym4", level=maxlev)
    for i in range(1, len(coeffs)):
        coeffs[i] = pywt.threshold(coeffs[i], thresh * max(coeffs[i]))
    return pywt.waverec(coeffs, "sym4")


def preprocess_axis(acc, mode=1):
    if mode == 1:
        fil_acc = butter_lowpass_filter(acc, 5, sample_rate)
        kernel_size = 5
        kernel = np.ones(kernel_size) / kernel_size  # Moving average
        filtered = np.convolve(fil_acc, kernel, mode="same")
        ds_acc = downsample_axis(filtered)
        return ds_acc
    elif mode == 2:
        wave_acc = wavelet_denoise(acc)
        kernel_size = 3
        kernel = np.ones(kernel_size) / kernel_size  # Moving average
        filtered = np.convolve(wave_acc, kernel, mode="same")
        ds_acc = downsample_axis(filtered)
        return ds_acc
    else:
        sm_acc = smoothen_axis(acc)
        ds_acc = downsample_axis(sm_acc)
        return ds_acc
    # return smoothen_axis(ds_acc)


def smoothen_axis(acc):
    denoise = sg.savgol_filter(acc, 21, 3, mode="nearest")  # Polynomial smoothing
    # kernel_size = 5
    # kernel = np.ones(kernel_size) / kernel_size  # Moving average
    # filtered = np.convolve(denoise, kernel, mode="same")
    return denoise


def downsample_axis(acc, factor=4):
    return acc[::factor]


def preprocess():
    for g in acc_gestures:
        templates = os.listdir(TEMPLATE_DIR + g)
        if not os.path.exists(PROC_DIR + g):
            os.mkdir(PROC_DIR + g)
        for t in templates:
            ts, at, acc_axes, _ = read_acc_data(TEMPLATE_DIR + g + "/" + t)

            sample_rate = 1 / ((ts[-1] - ts[0]) / len(ts))

            new_axes = [
                preprocess_axis(acc_axes[0]),
                preprocess_axis(
                    acc_axes[1],
                ),
                preprocess_axis(acc_axes[2]),
            ]

            # new_axes = []
            # for order in range(5, 50, 10):
            #     new_axes.append(
            #         [
            #             smoothen_axis(acc_axes[0], order=order),
            #             smoothen_axis(acc_axes[1], order=order),
            #             smoothen_axis(acc_axes[2], order=order),
            #         ]
            #     )

            write_acc_data(downsample_axis(ts), new_axes, downsample_axis(at), PROC_DIR + g + "/" + t)

            # fig = plt.figure()
            # plt.plot(ts, acc_axes[0], label="raw", c="grey")
            # for i in range(len(new_axes)):
            #     plt.plot(downsample_axis(ts), new_axes[i][0], label=str(i))
            plt.plot(ts, at)
            plt.plot(downsample_axis(ts), preprocess_axis(at, 2))
            plt.show()
            # break
            # plot_compare(ts, acc_axes, downsample_axis(ts), new_axes)
            # plt.title("Preprocessing Techniques: Comparison")
            # plt.legend()
            # plt.show()
            # plt.close()
            break
        break


preprocess()
