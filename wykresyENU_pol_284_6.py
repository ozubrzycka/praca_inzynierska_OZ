import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# Dane referencyjne:
refs = {
    "BOGO": {"E": 22066.760804089783, "N": 5042.613283347428,   "U": -16.15854886966008},
    "JOZ":  {"E": 22050.371146572237, "N": -37032.26064241033, "U": -118.7524486519178},
    "MIMA": {"E": 58049.0715139549,   "N": -27453.112025968803, "U": -247.6699704197854},
}

# Okresy:
days_info = [284, 285, 286]

stations = ["BOGO", "JOZ", "MIMA"]

station_colors = {"BOGO": "green", "JOZ": "red", "MIMA": "orange"}

all_data = {"E": [], "N": [], "U": []}
all_time = []
all_colors = []

for day_index, doy in enumerate(days_info):
    for st in stations:

        df_enu = pd.read_csv(f"ENU_NODW_{st}_{doy}.csv", header=None, names=["E","N","U"])
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

# Luka dla DOY 285:
# - pomiędzy 13:29:30 a 19:00:00 brak danych w pliku RINEX
# DOY 285 zaczyna się od 24h (DOY 284 to pierwsze 24h)
start_gap = 24 + 13 + 29/60 + 30/3600  # 24h + 13:29:30
end_gap   = 24 + 19                     # 24h + 19:00:00
gap_hours = end_gap - start_gap         # długość luki

mask_doy285 = (all_time >= 24) & (all_time < 48)
mask_after_gap = mask_doy285 & (all_time > start_gap)
all_time[mask_after_gap] += gap_hours

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

    plt.xlabel("Czas (h) — 3 dni (DOY 284, 285, 286)", fontsize=14)
    plt.ylabel(ylabel, fontsize=14)
    plt.grid(True)

    # Legenda według stacji
    legend_elements = [
        Line2D([0],[0], marker='o', color='w', label='BOGO00POL', markerfacecolor=station_colors["BOGO"], markersize=6),
        Line2D([0],[0], marker='o', color='w', label='JOZ200POL',  markerfacecolor=station_colors["JOZ"], markersize=6),
        Line2D([0],[0], marker='o', color='w', label='MIMA00POL', markerfacecolor=station_colors["MIMA"], markersize=6),
    ]
    plt.legend(handles=legend_elements, fontsize=10)
    plt.tight_layout()
    plt.show()

plot_component_station("E", "sigma E [m]")
plot_component_station("N", "sigma N [m]")
plot_component_station("U", "sigma U [m]")


