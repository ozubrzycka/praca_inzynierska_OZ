import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- wartości referencyjne ---
E_ref_CEBR = -10027.114672854777
E_ref_VILL = 25257.097054654892
E_ref_TOR  = 67612.36157869967

N_ref_CEBR = 2701.771231459912
N_ref_VILL = 1645.08125298489
N_ref_TOR = 5138.876225557352

U_ref_CEBR = -62.09812030468038
U_ref_VILL = -232.2427890090852
U_ref_TOR = -528.4575335533145

# Analizowane dni:
days_info = [
    {"doy": 284, "trim": {"CEBR":1, "VILL":1, "TOR":1}, "num_points": 2878},
    {"doy": 285, "trim": {"CEBR":1, "VILL":1, "TOR":1}, "num_points": 2878},
    {"doy": 286, "trim": {"CEBR":1, "VILL":1, "TOR":1}, "num_points": 2878},
]


all_cebr = []
all_vill = []
all_tor = []


for day in days_info:
    doy = day["doy"]
    trim = day["trim"]
    num_points = day["num_points"]
    
    df_cebr = pd.read_csv(f"ENU_MADR_CEBR_{doy}.csv", header=None, names=["E","N","U"])
    df_vill = pd.read_csv(f"ENU_MADR_VILL_{doy}.csv", header=None, names=["E","N","U"])
    df_tor  = pd.read_csv(f"ENU_MADR_TOR_{doy}.csv",  header=None, names=["E","N","U"])
    
    diff_cebr = abs(df_cebr["U"] - U_ref_CEBR)[:-trim["CEBR"]]
    diff_vill = abs(df_vill["U"] - U_ref_VILL)[:-trim["VILL"]]
    diff_tor  = abs(df_tor["U"] - U_ref_TOR)[:-trim["TOR"]]
    
    all_cebr.append(diff_cebr)
    all_vill.append(diff_vill)
    all_tor.append(diff_tor)


diff_cebr_all = pd.concat(all_cebr).reset_index(drop=True)
diff_vill_all = pd.concat(all_vill).reset_index(drop=True)
diff_tor_all  = pd.concat(all_tor).reset_index(drop=True)


total_points = len(diff_cebr_all)
time_hours = np.arange(total_points) * (30/3600)

# --- wykres ---
plt.figure(figsize=(14,6))

plt.scatter(time_hours, diff_vill_all, s=4, color="red", label="VILL00ESP")
plt.scatter(time_hours, diff_tor_all,  s=4, color="orange", label="TOR100ESP")
plt.scatter(time_hours, diff_cebr_all, s=4, color="green", label="CEBR00ESP")

plt.ylim(0, 1.6)
plt.yticks(np.arange(0, 1.61, 0.1))


# Pionowe linie rezgraniczające dni analizy:
for x in [24, 48]:
    plt.axvline(x=x, color='blue', linestyle='--', alpha=0.7) 
    
    
plt.xticks(np.arange(0, 75, 3))
plt.xlabel("Czas (h) — 3 dni (DOY 284, 285, 286)")
plt.ylabel("sigma E [m]")
#plt.title("Odchylenia składowej pionowej U (NEU) względem pozycji referencyjnej - DOY 284, 285, 286")

plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
