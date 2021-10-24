import numpy as np
import matplotlib.pyplot as plt

### for cross
# window = 7.5
# starts = [2.5, 11, 19, 26, 33, 40, 46.5, 53, 60, 66.5, 73]
### for wave
# window = 5
# starts = [1, 6, 11.5, 17.5, 23, 28.5, 33.5, 39, 44, 49.5, 55, 61, 66.5, 71.5, 76.5, 83]
### for fwd/bkwd
window = 5
starts = [2.5, 9, 16, 21, 27, 33, 39, 45, 51, 56.5, 62.5, 68, 74, 80.5, 86, 92, 97.5, 103, 110, 118, 123, 128, 134, 141]

gesture = "fwd_bkwd"
DATA_DIR = "raw_data/"
OUT_DIR = "raw_templates/"

num = len(starts)
print(num)
curr = 0
with open(DATA_DIR + gesture + ".csv", "r") as f:
    lines = f.readlines()
header = lines[0]
lines = lines[1:]
sets = []
for i in range(num):
    start = starts[i]
    with open(OUT_DIR + gesture + "/" + str(i + 1) + ".csv", "w") as f:
        f.write(header)
        vals = []
        for line in lines:
            ts, ax, ay, az, at = list(map(float, line.split(",")))
            if ts < start:
                continue
            elif ts > start + window:
                break
            else:
                f.write(",".join(map(str, [ts - start, ax, ay, az, at])) + "\n")
                vals.append([ts - start, at])
        sets.append(vals)

for i in range(int(num / 5)):
    for j in range(5):
        val = sets[i * 5 + j]
        ax = plt.subplot2grid((int(num / 5), 5), (i, j))
        ax.plot([i[0] for i in val], [i[1] for i in val])
plt.show()
