import folium
import numpy as np
import math

# Hypothèses pour accurate details_data
# LAT_MIN = 47.023456
# LAT_MAX = 47.923456
# LON_MIN = 6.123456
# LON_MAX = 6.123456

# square search area
LAT_MIN = 42.000074
LAT_MAX = 49.999974
LON_MIN = 0.000000
LON_MAX = 8.000000

DETAILS_DATA = False


def calculate_grid_points(lat_min, lat_max, lon_min, lon_max, details_data):
    if details_data:
        lat_diff_str, lon_diff_str = calculate_diffs(lat_min, lat_max, lon_min, lon_max)
        num_points_lat = calculate_points(lat_diff_str)
        num_points_lon = calculate_points(lon_diff_str)
    else:
        num_points_lat = 2
        num_points_lon = 2

    return np.linspace(lat_min, lat_max, num_points_lat), np.linspace(lon_min, lon_max, num_points_lon)


def calculate_diffs(lat_min, lat_max, lon_min, lon_max):
    lat_diff = round(lat_max - lat_min, 6)
    lon_diff = round(lon_max - lon_min, 6)

    lat_diff_micro = lat_diff * 10 ** 6
    lon_diff_micro = lon_diff * 10 ** 6

    lat_diff_str = str(int(lat_diff_micro))
    lon_diff_str = str(int(lon_diff_micro))

    return lat_diff_str, lon_diff_str


def calculate_points(diff_str):
    points_list = [int(digit) + 1 for digit in diff_str if digit != '0']
    return max(math.prod(points_list), 1)


def initialize_map(center, zoom=6):
    return folium.Map(location=center, zoom_start=zoom)


def add_grid_to_map(m, lat_points, lon_points):
    mid_lon = (LON_MIN + LON_MAX) / 2
    mid_lat = (LAT_MIN + LAT_MAX) / 2

    # Add grid points to the map with labels
    for lat in lat_points:
        for lon in lon_points:
            folium.Marker(
                [lat, lon],
                popup=f"Lat: {lat:.6f}, Lon: {lon:.6f}",
                icon=folium.Icon(color="blue", icon="info-sign")
            ).add_to(m)

    for lat in lat_points:
        folium.PolyLine([(lat, LON_MIN), (lat, LON_MAX)], color="blue", weight=1).add_to(m)
        folium.Marker(
            [lat, mid_lon],
            icon=folium.DivIcon(
                html=f'<div style="font-size: 12px; color: blue; margin-top: -10px;">Lat={lat:.6f}</div>')
        ).add_to(m)

    for lon in lon_points:
        folium.PolyLine([(LAT_MIN, lon), (LAT_MAX, lon)], color="green", weight=1).add_to(m)
        folium.Marker(
            [mid_lat, lon],
            icon=folium.DivIcon(
                html=f'<div style="font-size: 12px; color: green; transform: rotate(-90deg); margin-left: -10px;">Lon={lon:.6f}</div>')
        ).add_to(m)


def add_markers_and_lines(m):
    specific_points = [
        (46.15878834400968, -1.2718925504584946, "Enigme 1 chez Ré monde", 'fa-solid fa-1'),
        (50.721787866105565, 2.5337913136757573, "Enigme 2 les 3 Citrouilles", 'fa-solid fa-2')
    ]

    for lat, lon, popup, icon in specific_points:
        folium.Marker(
            [lat, lon],
            popup=popup,
            icon=folium.Icon(color='red', icon=icon)
        ).add_to(m)

    # Trace une ligne rouge entre les deux points spécifiques
    folium.PolyLine(
        locations=[(specific_points[0][0], specific_points[0][1]), (specific_points[1][0], specific_points[1][1])],
        color="red",
        weight=2,
    ).add_to(m)


def main():
    # Calcul des points de grille
    lat_points, lon_points = calculate_grid_points(LAT_MIN, LAT_MAX, LON_MIN, LON_MAX, DETAILS_DATA)

    # Calcul du centre de la carte
    map_center = [(LAT_MIN + LAT_MAX) / 2, (LON_MIN + LON_MAX) / 2]

    # Initialisation de la carte
    m = initialize_map(map_center)

    # Ajout des points de grille
    add_grid_to_map(m, lat_points, lon_points)

    # Ajout des marqueurs spécifiques et de la ligne entre eux
    add_markers_and_lines(m)

    # Sauvegarde de la carte
    m.save("gnss_quantique.html")
    print("The map with the grid and specific marker has been generated and saved as 'gnss_quantique.html'.")


if __name__ == "__main__":
    main()
