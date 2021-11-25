import numpy as np
import matplotlib.pyplot as plt
from timeit import default_timer as timer
from dtw_cosine import dtw
from dtw_variants import dtw_sakoe_chiba, fast_dtw, plot_alignment_with_variants
from preprocess import preprocess_axis, downsample_axis
import os
import warnings
from timeit import default_timer as timer

warnings.filterwarnings("ignore")

dtw = fast_dtw
score_thresh = 100

TEST_FILE = "test/online/test.csv"
# TEMPLATE_DIR = "raw_templates/"
TEMPLATE_DIR = "clean_templates/"

gestures = ["cross", "wave", "forward", "backward"]

templates = {}
window_size = 0
for g in gestures:
    templates[g] = []
    for filen in os.listdir(TEMPLATE_DIR + g):
        acc_total = []
        times = []
        acc_x, acc_y, acc_z = [], [], []
        with open(TEMPLATE_DIR + g + "/" + filen, "r") as f:
            lines = f.readlines()[1:]
            template_size = int(len(lines))
            window_size = max(template_size, window_size)
            for line in lines:
                ts, ax, ay, az, at = list(map(float, line.split(",")))[:5]
                times.append(ts)
                acc_total.append(at)
                acc_x.append(ax)
                acc_y.append(ay)
                acc_z.append(az)
        templates[g].append({"data": [acc_x, acc_y, acc_z], "time": times, "acc_total": acc_total})

window_size *= 4

test_file = open(TEST_FILE, "r")
line = test_file.readline()

max_lines = float(len(open(TEST_FILE, "r").readlines()))

data = [[], [], []]
atotal = []
times = []
ts = 0

end = False
num_lines = 0

start = int(input())

while num_lines < max_lines:
    for l in range(int(window_size / 4)):
        line = test_file.readline()
        # end = True
        # break
        try:
            ts, ax, ay, az, at = list(map(float, line.split(",")))
            num_lines += 1
        except:
            end = True
            print("Exiting")
            break

        times.append(ts)
        atotal.append(at)
        data[0].append(ax)
        data[1].append(ay)
        data[2].append(az)

        if l % 32 == 0:
            plt.clf()
            plt.plot(times, atotal, c="grey", label="raw")
            plt.legend()
            plt.pause(0.02)

    if end:
        plt.close()
        break

    if len(data[0]) < window_size:
        continue

    window = [data[0][-window_size:], data[1][-window_size:], data[2][-window_size:]]
    clean_window = [preprocess_axis(window[0]), preprocess_axis(window[1]), preprocess_axis(window[2])]

    if np.mean((atotal[-window_size:])) < 1.0:
        # print(np.mean(preprocess_axis(atotal[-window_size:])))
        # print("bruh")
        continue

    match = None
    match_g = None
    match_cm = None
    match_align = None
    match_cost = float("inf")

    plt.clf()
    plt.plot(times, atotal, c="grey", label="raw")
    plt.plot(
        downsample_axis(times[-window_size:]),
        preprocess_axis(atotal[-window_size:]),
        c="blue" if match_g is None else "red",
        label="window" if match_g is None else match_g,
    )
    plt.legend()
    plt.pause(0.2)

    start_time = timer()

    for g in gestures:
        best_t = None
        min_cm = None
        min_al = None
        avg_score = float("inf")
        g_score = float("inf")
        num_templates = 0

        for t in templates[g]:
            score, cm, al = dtw(t["data"], clean_window)
            if score > score_thresh:
                # print(score)
                continue
            elif avg_score > 0:
                avg_score = 0
                num_templates += 1
            avg_score += score
            if score < g_score:
                min_al = al
                min_cm = cm
                g_score = score
                best_t = t

        avg_score /= num_templates if num_templates > 0 else float("inf")
        # print(avg_score, match_cost)
        if avg_score < match_cost:
            # if g == "cross":
            # print(avg_score)
            match_cost = avg_score
            match_align = min_al
            match_cm = min_cm
            match = best_t
            match_g = g

    end_time = timer()

    # if match is not None:
    #     # print(match_align)
    #     plt.plot(
    #         range(len(match_align)),
    #         [clean_window[0][x] for (_, x) in match_align],
    #     )
    #     plt.plot(range(len(match_align)), [match["data"][0][x] for (x, _) in match_align])

    if match_g is None:
        continue

    print("Best Match:", match_g, "Cost: ", round(match_cost, 2), "Time Start: ", round(times[-window_size], 3))
    print("Current Time: ", round(times[-1], 3), "Compute Time: ", end_time - start_time)

    # plt.figure(2)
    plt.clf()
    plt.plot(times, atotal, c="grey", label="raw")
    plt.plot(
        downsample_axis(times[-window_size:]),
        preprocess_axis(atotal[-window_size:]),
        c="blue" if match_g is None else "red",
        label="window" if match_g is None else match_g,
    )
    plt.title(match_g)
    plt.legend()
    plt.pause(0.5)

    # if match is not None:
    # plt.plot([times[-window_size:][x] for (x, _) in match_align], [match["acc_total"][x] for (x, _) in match_align])
    # plot_alignment_with_variants(match_cm, match_align, clean_window, best_t["data"], sakoe_chiba=True, fig=2)

plt.show()
