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

def compute_roti(rot, window=20):
    return pd.Series(rot).rolling(window=window, min_periods=1).std().values


file_names = ["NODW284-2024-10-10.Cmn",
              "NODW285-2024-10-11.Cmn",
              "NODW286-2024-10-12.Cmn"]
start_hours = [0, 24, 48]  

rots_all = []
rotis_all = []
time_all = []

for fname, start_h in zip(file_names, start_hours):
    df = load_cmn(fname)

    if len(df) < 2:
        continue

    rot = compute_rot(df)
    roti = compute_roti(rot, window=20)
    t = np.arange(len(rot)) * (30/3600) + start_h  
    rots_all.append(rot)
    rotis_all.append(roti)
    time_all.append(t)

# Łączenie wszystkich dni
all_time = np.concatenate(time_all)
rots_full = np.concatenate(rots_all)
rotis_full = np.concatenate(rotis_all)

# Luka w DOY 285: 13:29:30–19:00
start_gap = 24 + 13 + 29/60 + 30/3600  
end_gap   = 24 + 19                     
gap_hours = end_gap - start_gap         

mask_doy285 = (all_time >= 24) & (all_time < 48)

mask_after_gap = mask_doy285 & (all_time > start_gap)
all_time[mask_after_gap] += gap_hours

# Wykres
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), sharex=True)

ax1.scatter(all_time, rots_full, s=3)
ax1.set_ylabel("ROT [TECU/min]", fontsize=16)         
ax1.set_ylim(-2.0, 2.0)
ax1.set_yticks(np.arange(-2.0, 2.01, 0.5))
ax1.tick_params(axis='y', labelsize=12)             
ax1.grid(True)

ax2.scatter(all_time, rotis_full, s=3)
ax2.set_ylabel("ROTI 5 min [TECU/min]", fontsize=16) 
ax2.set_ylim(0, 2.0)
ax2.set_yticks(np.arange(0, 2.01, 0.5))
ax2.tick_params(axis='y', labelsize=12)              
ax2.set_xlabel("Czas [h] (DOY 284, 285, 286)", fontsize=14) 
ax2.tick_params(axis='x', labelsize=12)             
ax2.grid(True)

ax2.set_xlim(0, 72)
ax2.set_xticks(np.arange(0, 73, 3))
for t in [24, 48]:
    ax1.axvline(t, color='red', linestyle='--', linewidth=1.2)
    ax2.axvline(t, color='red', linestyle='--', linewidth=1.2)

plt.tight_layout()
plt.show()
