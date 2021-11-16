import numpy as np
import matplotlib.pyplot as plt
from numpy.core.shape_base import block
from numpy.testing._private.utils import _assert_valid_refcount
from dtw_cosine import dtw, plot_alignment

TEST_FILE = "test/sensor.csv"
TEMPLATE_DIR = "raw_templates/"


def read_data(filename, show_plot=False):
    timestamps = []
    acc_total = []
    acc_x = []
    acc_y = []
    acc_z = []
    with open(filename, "r") as f:
        for line in f.readlines()[1:]:
            ts, ax, ay, az, at = list(map(float, line.split(",")))
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


def match():
    min_score = float("inf")
    alignment = None
    cost_matrix = None
    match_file = None
    match_gesture = None
    match_at = None
    gestures = ["cross", "forward", "wave"]
    num_templates = 2
    _, at_data, test_data, total_plot = read_data(TEST_FILE, show_plot=True)
    plt.show(block=False)
    for g in gestures:
        avg_score = 0
        min_al = None
        min_cm = None
        best_file = None
        best_at = None
        g_score = float("inf")
        for i in range(num_templates):
            template_file = TEMPLATE_DIR + g + "/" + str(i + 1) + ".csv"
            _, at, template, _ = read_data(template_file)
            score, cm, al = dtw(template, test_data)
            avg_score += score
            print(template_file + " : " + str(score))
            if score < g_score:
                min_al = al
                min_cm = cm
                g_score = score
                best_file = template_file
                best_at = at
        avg_score /= num_templates
        print("\nGesture: " + g + " Avg DTW score: " + str(avg_score) + "\n")
        if avg_score < min_score:
            min_score = score
            alignment = min_al
            cost_matrix = min_cm
            match_gesture = g
            match_file = best_file
            match_at = best_at
    print("Best Match: ", match_gesture)
    plot_alignment(cost_matrix, alignment, at_data, match_at)
    plt.show()


match()
