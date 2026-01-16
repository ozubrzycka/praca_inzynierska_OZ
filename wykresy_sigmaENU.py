import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# Dane referencyjne:
refs = {
    "HOA": {"E": -11717.483475578178, "N": 28170.439823906483, "U": -95.15530320150538},
    "TJU": {"E": -46126.442650128265, "N": 28082.640680199976, "U": -391.8129662269639},
    "ONSA": {"E": -58076.34517919862, "N": -35180.94558484411, "U": -536.3832816155409},
}

# Okres:
days_info = [131, 132, 133]

stations = ["HOA", "TJU", "ONSA"]

# Kolory stacji:
station_colors = {"HOA": "green", "TJU": "red", "ONSA": "orange"}

all_data = {"E": [], "N": [], "U": []}
all_time = []
all_colors = []

for day_index, doy in enumerate(days_info):
    for st in stations:

        df_enu = pd.read_csv(f"ENU_SPT_{st}_{doy}.csv", header=None, names=["E","N","U"])
        num_points_day = len(df_enu)

        colors = np.full(num_points_day, station_colors[st])

        time_day = np.arange(num_points_day) * (30/3600) + 24*day_index

        for comp in ["E","N","U"]:
            diff = df_enu[comp].values - refs[st][comp]
            all_data[comp].append(diff)

        all_time.append(time_day)
        all_colors.append(colors)

for comp in ["E","N","U"]:
    all_data[comp] = np.concatenate(all_data[comp])
all_time = np.concatenate(all_time)
point_colors = np.concatenate(all_colors)

# Wykres
def plot_component_station(comp, ylabel):
    min_len = min(len(all_time), len(all_data[comp]), len(point_colors))
    time = all_time[:min_len]
    data = all_data[comp][:min_len]
    colors = point_colors[:min_len]

    plt.figure(figsize=(14,6))
    plt.scatter(time, data, s=4, c=colors)

    plt.ylim(-2, 2)
    plt.yticks(np.arange(-2.0, 2.01, 0.5), fontsize=12)
    plt.xticks(np.arange(0, 75, 3), fontsize=12)

    # Linie pionowe dla dni
    for x in [24, 48]:
        plt.axvline(x=x, color='blue', linestyle='--', alpha=0.7)

    plt.xlabel("Czas (h) — 3 dni (DOY 131, 132, 133)", fontsize=14)
    plt.ylabel(ylabel, fontsize=14)
    plt.grid(True)

    # Legenda według stacji
    legend_elements = [
        Line2D([0],[0], marker='o', color='w', label='HOA000SWE', markerfacecolor=station_colors["HOA"], markersize=6),
        Line2D([0],[0], marker='o', color='w', label='TJU000SWE',  markerfacecolor=station_colors["TJU"], markersize=6),
        Line2D([0],[0], marker='o', color='w', label='ONSA00SWE', markerfacecolor=station_colors["ONSA"], markersize=6),
    ]
    plt.legend(handles=legend_elements, fontsize=10)
    plt.tight_layout()
    plt.show()

plot_component_station("E", "sigma E [m]")
plot_component_station("N", "sigma N [m]")
plot_component_station("U", "sigma U [m]")