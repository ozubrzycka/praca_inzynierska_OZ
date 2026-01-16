import matplotlib.pyplot as plt
import numpy as np

# Globalne ustawienia czcionek
plt.rcParams.update({
    "font.size": 12,
    "axes.labelsize": 16,
    "axes.titlesize": 18,
    "legend.fontsize": 12,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12
})

# Stacje
stations = ["CEBR00ESP","VILL00ESP","TOR100ESP",
            "BOGO00POL","JOZ200POL","MIMA00POL",
            "HOA000SWE","TJU000SWE","ONSA00SWE"]

# RMS_H dla DOY 284-286
RMS_H = np.array([[0.0395, 0.0136, 0.0172],
                  [0.1317, 0.0184, 0.0307],
                  [0.1266, 0.0264, 0.0336],
                  [0.0392, 0.0261, 0.0277],
                  [0.0668, 0.0178, 0.0242],
                  [0.0400, 0.0204, 0.0240],
                  [0.2470, 0.1069, 0.0142],
                  [0.2152, 0.0944, 0.0133],
                  [0.1986, 0.0661, 0.0106]])

# RMS_V dla DOY 284-286
RMS_V = np.array([[0.0461, 0.0207, 0.0276],
                  [0.1216, 0.0361, 0.0564],
                  [0.1044, 0.0554, 0.0801],
                  [0.0443, 0.0233, 0.0231],
                  [0.0785, 0.0371, 0.0189],
                  [0.0465, 0.0537, 0.0252],
                  [0.2930, 0.1469, 0.0243],
                  [0.2892, 0.1730, 0.1030],
                  [0.2836, 0.1382, 0.1384]])

days = ["DOY 284","DOY 285","DOY 286"]
x = np.arange(len(stations))
width = 0.25

# --- Wykres RMS_H ---
fig, ax = plt.subplots(figsize=(15, 6))
for i in range(3):
    ax.bar(x + (i - 1) * width, RMS_H[:, i], width, label=days[i])

ax.set_xticks(x)
ax.set_xticklabels(stations, rotation=45, ha="right")
ax.set_ylabel("RMS_H [m]", labelpad=10)
#ax.set_title("Błędy RMS pozycji poziomej — DOY 284–286")
ax.legend()
ax.grid(True)

plt.tight_layout()
plt.show()

# --- Wykres RMS_V ---
fig, ax = plt.subplots(figsize=(15, 6))
for i in range(3):
    ax.bar(x + (i - 1) * width, RMS_V[:, i], width, label=days[i])

ax.set_xticks(x)
ax.set_xticklabels(stations, rotation=45, ha="right")
ax.set_ylabel("RMS_V [m]", labelpad=10)
#ax.set_title("Błędy RMS pozycji wysokościowej — DOY 284–286")
ax.legend()
ax.grid(True)

plt.tight_layout()
plt.show()
