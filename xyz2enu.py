import numpy as np
import pandas as pd
from math import sin, cos, radians, sqrt

#%% 1. Funkcje:
    
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

def topocentrENU(X, Y, Z, lat_ref, lon_ref, h_ref):
    '''
    This function returns the position coordinates of a user at the WGS-84 ECEF coordiantes in east-north-up coordinates
    relative to the reference position located at lat_ref (latitude in degrees),     
    lon_ref (longitude in degrees) and h_ref (in meters).
    
    INPUT:
        X, y, Y : WGS-84 ECEF [meters] - target

        lat_ref             : [degrees] observer latitude,
        lon_ref             : [degrees] observer  longitude,
        h_ref               : [meters] observer altitude
    OUTPUT: 
        enu
    EXAMPLE: 
        enu = xyz2enu(p_e,lat_ref,lon_ref,h_ref)           
    '''
    #  convert lat, lon, h  to XYZ WGS84 
    XYZ_ref = plh2xyz(lat_ref, lon_ref, h_ref)
    delta_X = X - XYZ_ref[0]
    delta_Y = Y - XYZ_ref[1]
    delta_Z = Z - XYZ_ref[2]

    #  Calculate ENU coordinates
    East    = -sin(radians(lon_ref)) * delta_X + cos(radians(lon_ref)) * delta_Y
    North   = -sin(radians(lat_ref)) * cos(radians(lon_ref)) * delta_X - sin(radians(lat_ref)) * sin(radians(lon_ref)) * delta_Y + cos(radians(lat_ref)) * delta_Z
    Up      =  cos(radians(lat_ref)) * cos(radians(lon_ref)) * delta_X + cos(radians(lat_ref)) * sin(radians(lon_ref)) * delta_Y + sin(radians(lat_ref)) * delta_Z

    return(East, North, Up)

def plh2xyz(lat, lon, h):
    '''
    This method returns the position coordinate [X,Y,Z] given in the WGS-84 Earth Centered Earth Fixed
    (ECEF) coordinate  for a user located at the goedetic coordinates lat,lon and h. The units
    of the output position vector, p_e, are meters. latitude, longitude, altitude (reference
    elipsoid WGS-84)
    INPUT:
        reference elipsoid WGS-84
        lat : latitude [degree]
        lon : longitude [degree]
        h   : altitude [meter]

    OUTPUT:
        X,Y,Z  - geocentric coordinates
    '''
    RE_WGS84 = 6378137.0
    ECC = 0.081819190842621

    #   Compute East-West Radius of curvature at current position
    R_E = RE_WGS84/(sqrt(1. - (ECC * sin(radians(lat)))**2))
    #  Compute ECEF coordinates
    X = (R_E + h)*cos(radians(lat)) * cos(radians(lon))
    Y = (R_E + h)*cos(radians(lat)) * sin(radians(lon))
    Z = ((1 - ECC**2)*R_E + h)*sin(radians(lat))
    return(X, Y, Z)

#%% 2. Obliczenia
# Obliczenia wykonano na przykładzie stacji referencyjnej NODW00POL oraz pliku uzyskanego z TBC dla wektora NODW00POL -> MIMA00POL w dniu o DOY 286 
XYZ = [3645290.9676, 1378210.0919, 5032291.5487] # wspolrzedne geocentryczne NODW00POL

lat_ref, lon_ref, h_ref = xyz2latlonh(XYZ[0], XYZ[1], XYZ[2])

# wczytanie danych z plików uzyskanych z TBC
df = pd.read_csv("NODW_MIMA_286.csv") 


ENU_all = []
for idx, row in df.iterrows():
    print(idx, row["X (ECEF)"], row["Y (ECEF)"], row["Z (ECEF)"])
    #ENU = geo.topocentrENU(X, Y, Z, lat_ref, lon_ref, h_ref)
    ENU = topocentrENU(float(row["X (ECEF)"]), float(row["Y (ECEF)"]), float(row["Z (ECEF)"]), lat_ref, lon_ref, h_ref)
    ENU_all.append(ENU)
    


ENU_arr = np.array(ENU_all)
np.savetxt("ENU_NODW_MIMA_286.csv", ENU_arr, delimiter=",")

#sprawdzenie odległośc 2D
dist2D  = np.hypot(ENU_arr[:, 0], ENU_arr[:, 1]) # wektor długości N-1
d = np.linalg.norm(ENU_arr[:, :2], axis=1)

#%% 3. Obliczenie współrzędnych w układzie topocentrycznym ENU dla wszytskich stacji:
   
# MADR00ESP - stacja referencyjna
XYZ_MADR = [4849202.3940,  -360328.9929,  4114913.1862]
lat_ref_madr, lon_ref_madr, h_ref_madr = xyz2latlonh(XYZ_MADR[0], XYZ_MADR[1], XYZ_MADR[2])

# CEBR00ESP, VILL00ESP, TOR00ESP
ENU_CEBR = topocentrENU(4846664.9180,-370195.2000,4116929.5260, lat_ref_madr, lon_ref_madr, h_ref_madr)
ENU_VILL = topocentrENU(4849833.7962, -335049.1807, 4116014.8247, lat_ref_madr, lon_ref_madr, h_ref_madr)
ENU_TOR = topocentrENU(4850488.0460, -292625.7599, 4118482.2331, lat_ref_madr, lon_ref_madr, h_ref_madr)

# NODW00POL - stacja referencyjna
XYZ_NODW = [3645290.9676, 1378210.0919, 5032291.5487] 
lat_ref_nodw, lon_ref_nodw, h_ref_nodw = xyz2latlonh(XYZ_NODW[0], XYZ_NODW[1], XYZ_NODW[2])

# BOGO00POL, JOZ200POL, MIMA00POL
ENU_BOGO = topocentrENU(3633739.3000, 1397433.9000, 5035353.3000, lat_ref_nodw, lon_ref_nodw, h_ref_nodw)
ENU_JOZE = topocentrENU(3664880.9100, 1409190.3850, 5009618.2850, lat_ref_nodw, lon_ref_nodw, h_ref_nodw)
ENU_MIMA = topocentrENU(3644974.5486, 1440149.8909, 5015356.6564, lat_ref_nodw, lon_ref_nodw, h_ref_nodw)

# SPT700SWE - stacja referencyjna 
XYZ_SPT = [3328988.6610, 761917.7752, 5369031.4815] 
lat_ref_spt, lon_ref_spt, h_ref_spt = xyz2latlonh(XYZ_SPT[0], XYZ_SPT[1], XYZ_SPT[2])

# HOA000SWE, TJU000SWE, ONSA00SWE
ENU_HOA = topocentrENU(3308338.3078, 745170.9879, 5383997.7832, lat_ref_spt, lon_ref_spt, h_ref_spt)
ENU_TJU = topocentrENU(3315933.0046, 711610.5328, 5383700.0922, lat_ref_spt, lon_ref_spt, h_ref_spt)
ENU_ONSA = topocentrENU(3370658.8291, 711876.9374, 5349786.7382, lat_ref_spt, lon_ref_spt, h_ref_spt)


