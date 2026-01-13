import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Wartoci referencyjne wspolrzednych topocentrycznych E/N:

E_ref_HOA = -11717.483475578178
E_ref_TJU = -46126.442650128265
E_ref_ONSA  = -58076.34517919862

N_ref_HOA = 28170.439823906483
N_ref_TJU = 28082.640680199976
N_ref_ONSA = -35180.94558484411


E_ref = {
    "HOA": -11717.483475578178,
    "TJU": -46126.442650128265,
    "ONSA": -58076.34517919862
}

N_ref = {
    "HOA": 28170.439823906483,
    "TJU": 28082.640680199976,
    "ONSA": -35180.94558484411
}

stations = ["HOA", "TJU", "ONSA"]

day_sets = {
    "131–133": [131, 132, 133],
    "284–286": [284, 285, 286]
}


all_E = []
all_N = []

for days in day_sets.values():
    for day in days:
        for st in stations:

            df = pd.read_csv(
                f"ENU_SPT_{st}_{day}.csv",
                header=None,
                names=["E", "N", "U"]
            )[:-1]

            all_E.extend(df["E"] - E_ref[st])
            all_N.extend(df["N"] - N_ref[st])

# maksymalna wartość bezwzględna
max_val = max(
    abs(min(all_E)), abs(max(all_E)),
    abs(min(all_N)), abs(max(all_N))
)

margin = 0.05 * max_val  # 5% marginesu
lim = max_val + margin

# Wykresy:

for set_name, days in day_sets.items():
    for st in stations:
        for day in days:

            df = pd.read_csv(
                f"ENU_SPT_{st}_{day}.csv",
                header=None,
                names=["E", "N", "U"]
            )[:-1]

            diff_E = df["E"] - E_ref[st]
            diff_N = df["N"] - N_ref[st]

            plt.figure(figsize=(8, 8))
            plt.xlabel("σE [m]", fontsize=12)
            plt.ylabel("σN [m]", fontsize=12)
            plt.grid(True)

            plt.scatter(diff_E, diff_N, s=5, color="black")

            # IDENTYCZNE OSIE DLA WSZYSTKICH
            plt.xlim(-1.5, 1.5)
            plt.ylim(-1.5, 1.5)

            # OSIE ZEROWE (NIEBIESKIE, PRZERYWANE)
            plt.axhline(0, color="blue", linestyle="--", linewidth=1.2)
            plt.axvline(0, color="blue", linestyle="--", linewidth=1.2)

            plt.gca().set_aspect("equal", adjustable="box")
            plt.tight_layout()
            plt.show()

