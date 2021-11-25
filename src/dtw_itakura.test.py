import numpy as np
import matplotlib.pyplot as plt
from timeit import default_timer as timer
from dtw_variants import dtw_itakura, plot_alignment_with_variants
from tqdm import tqdm
from preprocess import preprocess_axis

TEST_FILE = "test/sensor.csv"
# TEMPLATE_DIR = "raw_templates/"
# TIME_FILE = "times/dtw_itakura.txt"
TEMPLATE_DIR = "clean_templates/"
TIME_FILE = "times/dtw_itakura_clean.txt"
NUM_RUNS = 100


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


def match_dtw_sc():
    min_score = float("inf")
    alignment = None
    cost_matrix = None
    match_file = None
    match_gesture = None
    match_at = None

    gestures = ["wave", "cross"]
    num_templates = 1

    _, at_data, raw_data, total_plot = read_acc_data(TEST_FILE, show_plot=False)
    test_data = [preprocess_axis(raw_data[0]), preprocess_axis(raw_data[1]), preprocess_axis(raw_data[2])]
    # test_data = raw_data

    with open(TIME_FILE, "a+") as f:
        if not open(TIME_FILE, "r").readlines():
            f.write("len_x, len_y, time\n")
        for g in gestures:
            avg_score = 0
            min_al = None
            min_cm = None
            best_file = None
            best_at = None
            g_score = float("inf")

            for i in range(num_templates):
                template_file = TEMPLATE_DIR + g + "/" + str(i + 1) + ".csv"
                _, at, template, _ = read_acc_data(template_file)

                elapse = 0
                for i in tqdm(range(NUM_RUNS)):
                    start = timer()
                    score, cm, al = dtw_itakura(template, test_data)
                    end = timer()
                    elapse += end - start
                f.write(("{},{},{}\n".format(len(at), len(test_data[0]), elapse / 100)))

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
        plot_alignment_with_variants(cost_matrix, alignment, at_data, match_at, itakura=True)
        plt.show()


match_dtw_sc()
