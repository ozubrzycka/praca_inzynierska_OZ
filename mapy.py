# -*- coding: utf-8 -*-
"""
Created on Sun Nov 23 10:52:50 2025

@author: ozubr
"""

import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature


# 1. Wykorzystna funkcja: XYZ -> lat, lon, h
def xyz2latlonh(X: float, Y: float, Z: float,
               a: float = 6378137.0, f: float = 1 / 298.257222101) -> tuple[float, float, float]:
    """
    Convert geocentric coordinates (X, Y, Z) to geodetic latitude, longitude,
    and ellipsoidal height using the Hirvonen iterative algorithm.

    Parameters
    ----------
    X, Y, Z : float
        Geocentric coordinates in meters.
    a : float, optional
        Semi-major axis of the reference ellipsoid (default: WGS84/GRS80 = 6378137.0 m).
    f : float, optional
        Flattening of the ellipsoid (default: 1/298.257222101 for GRS80).
    tol : float, optional
        Convergence tolerance on latitude in radians (default: 1e-12).
    max_iter : int, optional
        Maximum number of iterations allowed (default: 10).

    Returns
    -------
    lat_deg : float
        Geodetic latitude in decimal degrees.
    lon_deg : float
        Geodetic longitude in decimal degrees (range −180 … +180).
    h : float
        Ellipsoidal height above the ellipsoid in meters.

    Notes
    -----
    * First eccentricity squared is computed as e² = 2f − f².
    * Iteration stops when successive latitude values differ by less than `tol`,
      or when `max_iter` is reached.
    * Longitude is computed directly from arctan2(Y, X).
    """
    TOLERANCE =  1e-12
    MAX_ITER = 10
    # 1. Compute first eccentricity squared
    e2 = 2 * f - f**2

    # 2. Longitude (no iteration required)
    lon = np.arctan2(Y, X)

    # 3. Distance from Z-axis
    p = np.hypot(X, Y)

    # 4. Initial latitude estimate
    lat = np.arctan2(Z, p * (1 - e2))

    # 5. Iterate latitude with Hirvonen formula
    lat_prev = 0.0
    it = 0
    while abs(lat - lat_prev) > TOLERANCE and it < MAX_ITER:
        lat_prev = lat
        # Radius of curvature in the prime vertical
        N = a / np.sqrt(1 - e2 * np.sin(lat) ** 2)
        # Compute ellipsoidal height
        h = p / np.cos(lat) - N
        # Update latitude estimate
        lat = np.arctan2(Z, p * (1 - e2 * N / (N + h)))
        it += 1

    # 6. Final values of N and h after iteration
    N = a / np.sqrt(1 - e2 * np.sin(lat) ** 2)
    h = p / np.cos(lat) - N

    # 7. Convert to degrees
    lat_deg = np.degrees(lat)
    lon_deg = np.degrees(lon)

    return lat_deg, lon_deg, h

# 1. Współrzędne stacji
stations = {
    # --- Hiszpania ---
    "MADR00ESP": (4849202.3940, -360328.9929, 4114913.1862),
    "CEBR00ESP": (4846664.9180, -370195.2000, 4116929.5260),
    "VILL00ESP": (4849833.7962, -335049.1807, 4116014.8247),
    "TOR100ESP": (4850488.0460, -292625.7599, 4118482.2331),
    # --- Polska ---
    "NODW00POL": (3645290.9676, 1378210.0919, 5032291.5487),
    "BOGO00POL": (3633739.3000, 1397433.9000, 5035353.3000),
    "MIMA00POL": (3644974.5486, 1440149.8909, 5015356.6564),
    "JOZ200POL": (3664880.9100, 1409190.3850, 5009618.2850),
    # --- Szwecja ---
    "SPT700SWE": (3328988.6610, 761917.7752, 5369031.4815),
    "HOA000SWE": (3308338.3078, 745170.9879, 5383997.7832),
    "TJU000SWE": (3315933.0046, 711610.5328, 5383700.0922),
    "ONSA00SWE": (3370658.8291, 711876.9374, 5349786.7382)
}

# 2. Konwersja na geograficzne
station_locs = {}
for name, (x, y, z) in stations.items():
    lat, lon, h = xyz2latlonh(x, y, z)
    station_locs[name] = (lat, lon)


# 3. Funkcja rysująca mapę
def draw_map(region_name, stations_subset, extent, country_labels=None, legend_loc='upper right'):
    plt.figure(figsize=(8, 8))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_extent(extent)

    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.BORDERS, linewidth=0.5)
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)

    cmap = plt.get_cmap('tab20', len(stations_subset))
    colors = [cmap(i) for i in range(len(stations_subset))]

    for name, color in zip(stations_subset, colors):
        lat, lon = station_locs[name]
        ax.plot(lon, lat, marker='o', color=color, markersize=8, transform=ccrs.PlateCarree())
        ax.plot([], [], 'o', color=color, label=name)

    ax.legend(title="Stacje GNSS", loc=legend_loc)

    if country_labels:
        for country, (lat, lon) in country_labels.items():
            ax.text(
                lon, lat, country, fontsize=12, fontweight='bold',
                transform=ccrs.PlateCarree(),
                bbox=dict(facecolor='white', alpha=0.6, edgecolor='none')
            )

    plt.title(region_name)
    plt.show()


# 4. Mapy
#Europa
draw_map(
    " ",
    list(stations.keys()),
    extent=[-15, 30, 35, 70],
    country_labels={"Hiszpania": (40, -3), "Polska": (52, 15), "Szwecja": (60, 15)},
    legend_loc='upper left'
)

#Hiszpania
draw_map(
    " ",
    ["MADR00ESP", "CEBR00ESP", "VILL00ESP", "TOR100ESP"],
    extent=[-10, 0, 35, 45],
    country_labels={"Hiszpania": (40, -3)}
)

#Polska
draw_map(
    " ",
    ["NODW00POL", "BOGO00POL", "MIMA00POL", "JOZ200POL"],
    extent=[14, 26, 48, 56],
    country_labels={"Polska": (52, 19)}
)

#Szwecja
draw_map(
    " ",
    ["SPT700SWE", "HOA000SWE", "TJU000SWE", "ONSA00SWE"],
    extent=[8, 20, 54, 65],
    country_labels={"Szwecja": (60, 15)}
)
