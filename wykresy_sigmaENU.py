import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Wartosci referencyjne współrzędnych stacji:
E_ref_HOA = -11717.483475578178
E_ref_TJU = -46126.442650128265
E_ref_ONSA  = -58076.34517919862

N_ref_HOA = 28170.439823906483
N_ref_TJU = 28082.640680199976
N_ref_ONSA = -35180.94558484411

U_ref_HOA = -95.15530320150538
U_ref_TJU = -391.8129662269639
U_ref_ONSA = -536.3832816155409

# Analizowane dni:
days_info = [
    {"doy": 284, "trim": {"CEBR":1, "VILL":1, "TOR":1}, "num_points": 2879},
    {"doy": 285, "trim": {"CEBR":1, "VILL":1, "TOR":1}, "num_points": 2879},
    {"doy": 286, "trim": {"CEBR":1, "VILL":1, "TOR":1}, "num_points": 2879},
]

all_cebr = []
all_vill = []
all_tor = []

for day in days_info:
    doy = day["doy"]
    trim = day["trim"]
    num_points = day["num_points"]
    
    df_cebr = pd.read_csv(f"ENU_SPT_HOA_{doy}.csv", header=None, names=["E","N","U"])
    df_vill = pd.read_csv(f"ENU_SPT_TJU_{doy}.csv", header=None, names=["E","N","U"])
    df_tor  = pd.read_csv(f"ENU_SPT_ONSA_{doy}.csv",  header=None, names=["E","N","U"])
    
    diff_cebr = (df_cebr["N"] - N_ref_HOA)[:-trim["CEBR"]]
    diff_vill = (df_vill["N"] - N_ref_TJU)[:-trim["VILL"]]
    diff_tor  = (df_tor["N"] - N_ref_ONSA)[:-trim["TOR"]]
    
    all_cebr.append(diff_cebr)
    all_vill.append(diff_vill)
    all_tor.append(diff_tor)


diff_cebr_all = pd.concat(all_cebr).reset_index(drop=True)
diff_vill_all = pd.concat(all_vill).reset_index(drop=True)
diff_tor_all  = pd.concat(all_tor).reset_index(drop=True)

total_points = len(diff_cebr_all)
time_hours = np.arange(total_points) * (30/3600)

# Wykres:
plt.figure(figsize=(14,6))

plt.scatter(time_hours, diff_vill_all, s=4, color="red", label="TJU000SWE")
plt.scatter(time_hours, diff_tor_all,  s=4, color="orange", label="ONSA00SWE")
plt.scatter(time_hours, diff_cebr_all, s=4, color="green", label="HOA000SWE")

plt.ylim(-2, 2)
plt.yticks(np.arange(-2.0, 2.01, 0.5), fontsize=12)
plt.xticks(np.arange(0, 75, 3), fontsize=12)
plt.yticks(np.arange(-2.0, 2.01, 0.5), fontsize=12)


# Pionowe linie przerywane - podział na 3 analizowane dni:
for x in [24, 48]:
    plt.axvline(x=x, color='blue', linestyle='--', alpha=0.7) 
    

plt.xticks(np.arange(0, 75, 3))
plt.xlabel("Czas (h) — 3 dni (DOY 284, 285, 286)", fontsize=14)
plt.ylabel("sigma N [m]", fontsize=14)
#plt.title("Odchylenia składowej pionowej U (NEU) względem pozycji referencyjnej - DOY 284, 285, 286")

plt.grid(True)
plt.legend(fontsize=12)
plt.tight_layout()
plt.show()
