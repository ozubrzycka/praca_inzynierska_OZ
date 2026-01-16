import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
colors_fixed = {"HOA": "green", "TJU": "limegreen", "ONSA": "springgreen"}
color_float = "black"


all_data = {"E": [], "N": [], "U": []}
all_time = []
all_colors = []

for day_index, doy in enumerate(days_info):
    for st in stations:
        # Wczytaj ENU
        df_enu = pd.read_csv(f"ENU_SPT_{st}_{doy}.csv", header=None, names=["E","N","U"])
        num_points_day = len(df_enu)
        
        df_status = pd.read_csv(f"SPT_{st}_{doy}.csv")
        status = df_status["GNSS Vector Observation.Solution Type"].values
        
        colors = [colors_fixed[st] if s=="Fixed" else color_float for s in status]
        
        for comp in ["E","N","U"]:
            diff = df_enu[comp].values - refs[st][comp]
            all_data[comp].append(diff)
        
        time_day = np.arange(num_points_day) * (30/3600) + 24*day_index
        all_time.append(time_day)
        
        all_colors.append(colors)

for comp in ["E","N","U"]:
    all_data[comp] = np.concatenate(all_data[comp])
all_time = np.concatenate(all_time)
point_colors = np.concatenate(all_colors)

# Wykres:
def plot_component(comp, ylabel):
    # Przytnij do najmniejszej długości
    min_len = min(len(all_time), len(all_data[comp]), len(point_colors))
    time = all_time[:min_len]
    data = all_data[comp][:min_len]
    colors = point_colors[:min_len]
    
    plt.figure(figsize=(14,6))
    scatter = plt.scatter(time, data, s=4, c=colors)
    
    plt.ylim(-2, 2)
    plt.yticks(np.arange(-2.0, 2.01, 0.5), fontsize=12)
    plt.xticks(np.arange(0, 75, 3), fontsize=12)
    
    for x in [24, 48]:
        plt.axvline(x=x, color='blue', linestyle='--', alpha=0.7)
    
    plt.xlabel("Czas (h) — 3 dni (DOY 131, 132, 133)", fontsize=14)
    plt.ylabel(ylabel, fontsize=14)
    plt.grid(True)
    
    # Legenda Fixed/Float
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label='HOA00SWE Fixed', markerfacecolor=colors_fixed["HOA"], markersize=6),
        Line2D([0], [0], marker='o', color='w', label='TJU00SWE Fixed', markerfacecolor=colors_fixed["TJU"], markersize=6),
        Line2D([0], [0], marker='o', color='w', label='ONSA00SWE Fixed', markerfacecolor=colors_fixed["ONSA"], markersize=6),
        Line2D([0], [0], marker='o', color='w', label='Float', markerfacecolor=color_float, markersize=6),
    ]
    plt.legend(handles=legend_elements, fontsize=12)
    
    plt.tight_layout()
    plt.show()

plot_component("E", "sigma E [m]")
plot_component("N", "sigma N [m]")
plot_component("U", "sigma U [m]")
