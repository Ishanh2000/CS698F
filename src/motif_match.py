import numpy as np
import matplotlib.pyplot as plt
from plot import plot_acc_data
import stumpy
import matplotlib.dates as dates
from matplotlib.patches import Rectangle

timestamps, acc_total, (acc_x, acc_y, acc_z), _ = plot_acc_data("wave.csv")
window = 500
profile = stumpy.stump(acc_total, window)
motif_idx = np.argsort(profile[:, 0])[0]
nearest_neighbor_idx = profile[motif_idx, 1]

fig, axs = plt.subplots(2, sharex=True, gridspec_kw={"hspace": 0})
plt.suptitle("Motif (Pattern) Discovery", fontsize="30")

axs[0].plot(acc_total)
axs[0].set_ylabel("Acc", fontsize="20")
rect = Rectangle((motif_idx, 0), window, 40, facecolor="lightgrey")
axs[0].add_patch(rect)
rect = Rectangle((nearest_neighbor_idx, 0), window, 40, facecolor="lightgrey")
axs[0].add_patch(rect)
axs[1].set_xlabel("Time", fontsize="20")
axs[1].set_ylabel("Matrix Profile", fontsize="20")
axs[1].axvline(x=motif_idx, linestyle="dashed")
axs[1].axvline(x=nearest_neighbor_idx, linestyle="dashed")
axs[1].plot(profile[:, 0])
plt.show()
