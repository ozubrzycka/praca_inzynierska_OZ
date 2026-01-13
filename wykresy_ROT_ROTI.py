import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def load_cmn(path):
    rows = []
    with open(path) as f:
        started = False
        for line in f:
            if line.startswith("MJdatet"):
                started = True
                continue
            if started:
                parts = line.split()
                if len(parts) >= 10:
                    rows.append(parts)
    cols = ["MJdatet", "Time", "PRN", "Az", "Ele", "Lat", "Lon", "Stec", "Vtec", "S4"]
    df = pd.DataFrame(rows, columns=cols)
    df = df.apply(pd.to_numeric, errors='coerce')
    return df

def compute_rot(df):
    v = df["Vtec"].values
    rot = np.diff(v) * 60 / 30.0 
    return rot

def compute_roti(rot, window=10):
    """ROTI = odchylenie standardowe ROT w interwale window próbek (5 min = 10 próbek)"""
    roti = pd.Series(rot).rolling(window=window, min_periods=1).std().values
    return roti


file_names = ["SPT7131-2024-05-10.Cmn", "SPT7132-2024-05-11.Cmn", "SPT7133-2024-05-12.Cmn"]
start_hours = [0, 24, 48]  

rots_all = []
rotis_all = []
time_all = []

for fname, start_h in zip(file_names, start_hours):
    df = load_cmn(fname)
    rot = compute_rot(df)
    roti = compute_roti(rot, window=10)
    
    t = np.arange(len(rot)) * (30/3600) + start_h  
    
    rots_all.append(rot)
    rotis_all.append(roti)
    time_all.append(t)

time_full = np.concatenate(time_all)
rots_full = np.concatenate(rots_all)
rotis_full = np.concatenate(rotis_all)

# Wykresy:
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), sharex=True)

# ROT:
ax1.scatter(time_full, rots_full, s=3, label="ROT (Rate of TEC)")
ax1.set_ylabel("ROT [TECU/min]")
ax1.grid(True)


# ROTI:
ax2.scatter(time_full, rotis_full, s=3, label="ROTI (std 5 min)")
ax2.set_ylabel("ROTI 5 min [TECU/min]")
ax2.set_xlabel("Czas [h] (DOY 131, 132, 133)")
ax2.grid(True)

# ROT – ustawienia osi Y
ax1.set_ylim(-2.0, 2.0)
ax1.set_yticks(np.arange(-2.0, 2.01, 0.5))

# ROTI – ustawienia osi Y
ax2.set_ylim(0, 2.0)
ax2.set_yticks(np.arange(0, 2.01, 0.5))

# Oś X: 0-72 h, tick co 3 h
ax2.set_xlim(0, 72)
ax2.set_xticks(np.arange(0, 73, 3))

# Pionowe linie na 24h i 48h
for t in [24, 48]:
    ax1.axvline(t, color='red', linestyle='--', linewidth=1.2)
    ax2.axvline(t, color='red', linestyle='--', linewidth=1.2)

plt.tight_layout()
plt.show()

