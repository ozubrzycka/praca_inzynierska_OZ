import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({
    "font.size": 12,
    "axes.labelsize": 16,
    "axes.titlesize": 18,
    "legend.fontsize": 12,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12
})

# Nazwy stacji:
stations = ["CEBR00ESP","VILL00ESP","TOR100ESP",
            "BOGO00POL","JOZ200POL","MIMA00POL",
            "HOA000SWE","TJU000SWE","ONSA00SWE"]

# RMS_H dla DOY 131-133
RMS_H = np.array([[0.0219, 0.0149, 0.0215],
                  [0.0451, 0.0186, 0.0508],
                  [0.0654, 0.0205, 0.0408],
                  [0.0661, 0.0256, 0.0270],
                  [0.0717, 0.0198, 0.0189],
                  [0.0690, 0.0197, 0.0201],
                  [0.1675, 0.1371, 0.0194],
                  [0.1470, 0.1313, 0.0126],
                  [0.1810, 0.1569, 0.0120]])

# RMS_V dla DOY 131-133
RMS_V = np.array([[0.0330, 0.0256, 0.0339],
                  [0.0468, 0.0401, 0.0507],
                  [0.0631, 0.0468, 0.0553],
                  [0.0527, 0.0246, 0.0201],
                  [0.0778, 0.0291, 0.0233],
                  [0.0748, 0.0333, 0.0290],
                  [0.2045, 0.1986, 0.0250],
                  [0.2302, 0.2051, 0.0893],
                  [0.2296, 0.2143, 0.1381]])

days = ["DOY 131", "DOY 132", "DOY 133"]
x = np.arange(len(stations))
width = 0.25

# Wykresy:
fig, ax = plt.subplots(figsize=(15, 6))
for i in range(3):
    ax.bar(x + (i - 1) * width, RMS_H[:, i], width, label=days[i])

ax.set_xticks(x)
ax.set_xticklabels(stations, rotation=45, ha="right")
ax.set_ylabel("RMS_H [m]", labelpad=10)
#ax.set_title("Błędy RMS pozycji poziomej — DOY 131–133")
ax.legend()
ax.grid(True)

plt.tight_layout()
plt.show()


fig, ax = plt.subplots(figsize=(15, 6))
for i in range(3):
    ax.bar(x + (i - 1) * width, RMS_V[:, i], width, label=days[i])

ax.set_xticks(x)
ax.set_xticklabels(stations, rotation=45, ha="right")
ax.set_ylabel("RMS_V [m]", labelpad=10)
#ax.set_title("Błędy RMS pozycji wysokościowej — DOY 131–133")
ax.legend()
ax.grid(True)

plt.tight_layout()
plt.show()
