import folium
import numpy as np
import math


class DetailedData:
    """Class representing the detailed search area."""
    LAT_MIN = 47.923884
    LAT_MAX = 49.923884
    LON_MIN = 0.923675
    LON_MAX = 8.923675


class SquareArea:
    """Class representing the broader square search area."""
    LAT_MIN = 47.000884
    LAT_MAX = 49.999884
    LON_MIN = 0.000675
    LON_MAX = 8.000675


def get_position(use_detailed_data):
    """Returns the position class based on the configuration."""
    return DetailedData() if use_detailed_data else SquareArea()


def calculate_grid_points(lat_min, lat_max, lon_min, lon_max, use_detailed_data):
    """Calculates grid points for latitude and longitude based on the given area."""
    if use_detailed_data:
def calculate_grid_points(lat_min, lat_max, lon_min, lon_max, use_detailed_data):
    """Calculates grid points for latitude and longitude based on the given area."""
    if use_detailed_data:
        lat_diff_str, lon_diff_str = calculate_diffs(lat_min, lat_max, lon_min, lon_max)
        num_points_lat = calculate_points(lat_diff_str)
        num_points_lon = calculate_points(lon_diff_str)
    else:
        num_points_lat = 2
        num_points_lon = 2

    return np.linspace(lat_min, lat_max, num_points_lat), np.linspace(lon_min, lon_max, num_points_lon)


def calculate_diffs(lat_min, lat_max, lon_min, lon_max):
    """Calculates differences in latitude and longitude as strings of microdegrees."""
    lat_diff_micro = int(round((lat_max - lat_min) * 1e6))
    lon_diff_micro = int(round((lon_max - lon_min) * 1e6))
    return str(lat_diff_micro), str(lon_diff_micro)
    """Calculates differences in latitude and longitude as strings of microdegrees."""
    lat_diff_micro = int(round((lat_max - lat_min) * 1e6))
    lon_diff_micro = int(round((lon_max - lon_min) * 1e6))
    return str(lat_diff_micro), str(lon_diff_micro)


def calculate_points(diff_str):
    """Calculates the number of points based on the difference string."""
    """Calculates the number of points based on the difference string."""
    points_list = [int(digit) + 1 for digit in diff_str if digit != '0']
    return max(math.prod(points_list), 1)


def initialize_map(center, zoom=6):
    """Initializes and returns a folium map centered at the given coordinates."""
    """Initializes and returns a folium map centered at the given coordinates."""
    return folium.Map(location=center, zoom_start=zoom)


def add_grid_to_map(m, lat_points, lon_points, position):
    """Adds grid points and lines to the map."""
    mid_lon = (position.LON_MIN + position.LON_MAX) / 2
    mid_lat = (position.LAT_MIN + position.LAT_MAX) / 2
def add_grid_to_map(m, lat_points, lon_points, position):
    """Adds grid points and lines to the map."""
    mid_lon = (position.LON_MIN + position.LON_MAX) / 2
    mid_lat = (position.LAT_MIN + position.LAT_MAX) / 2

    for lat in lat_points:
        for lon in lon_points:
            folium.Marker(
                [lat, lon],
                popup=f"Lat: {lat:.6f}, Lon: {lon:.6f}",
                icon=folium.Icon(color="blue", icon="info-sign")
            ).add_to(m)

        folium.PolyLine([(lat, position.LON_MIN), (lat, position.LON_MAX)], color="blue", weight=1).add_to(m)
        folium.PolyLine([(lat, position.LON_MIN), (lat, position.LON_MAX)], color="blue", weight=1).add_to(m)
        folium.Marker(
            [lat, mid_lon],
            icon=folium.DivIcon(
                html=f'<div style="font-size: 12px; color: blue; margin-top: -10px;">Lat={lat:.6f}</div>')
        ).add_to(m)

    for lon in lon_points:
        folium.PolyLine([(position.LAT_MIN, lon), (position.LAT_MAX, lon)], color="green", weight=1).add_to(m)
        folium.PolyLine([(position.LAT_MIN, lon), (position.LAT_MAX, lon)], color="green", weight=1).add_to(m)
        folium.Marker(
            [mid_lat, lon],
            icon=folium.DivIcon(
                html=f'<div style="font-size: 12px; color: green; transform: rotate(-90deg); margin-left: -10px;">Lon={lon:.6f}</div>')
        ).add_to(m)


def add_markers_and_lines(m):
    """Adds specific markers and lines between them to the map."""
    """Adds specific markers and lines between them to the map."""
    specific_points = [
        (46.15878834400968, -1.2718925504584946, "Enigme 1 chez Ré monde", 'fa-solid fa-1'),
        (50.721787866105565, 2.5337913136757573, "Enigme 2 les 3 Citrouilles", 'fa-solid fa-2'),
        (47.47327153775195, -0.5550084763123877, "Enigme 3 La Glacerie d'Anjou", 'fa-solid fa-3'),
        (46.141782734484735, 1.879348485208694, "Enigme 4 La Pierre Mystere", 'fa-solid fa-4'),
        (43.61277522184278, 3.879513380408009, "Enigme 5 AlphaNef", 'fa-solid fa-5'),
        (49.67185797928755, 4.842056015264417, "Enigme 6 Chapelle Saint-Roger", 'fa-solid fa-6'),
        (43.04395371366447, 1.6122175124976217, "Enigme 7 Ariège", 'fa-solid fa-7'),
        (48.844205330061065, 2.4409678344258494, "Enigme 8 Île-de-France", 'fa-solid fa-8'),
        (47.31923053435358, 5.151234077316385, "Enigme 9 Côte-d'Or", 'fa-solid fa-9'),
        (48.57201706001636, 7.763461001088638, "Enigme 10 Entre Nancy et Strasbourg", 'fa-solid fa-a'),
        (47.39295503316493, 0.7253534677575671, "Enigme 11 Indre-et-Loire", 'fa-solid fa-b'),
        (48.01121029245369, -3.942390947484212, "Enigme 12 Bretagne", 'fa-solid fa-c'),
        (46.988458091474726, 6.936595661085478, "Enigme 13 Suisse", 'fa-solid fa-d'),
        (45.765560847282806, 4.828959507897815, "Enigme 14 Lyon", 'fa-solid fa-e'),


    ]

    for lat, lon, popup, icon in specific_points:
        folium.Marker(
            [lat, lon],
            popup=popup,
            icon=folium.Icon(color='red', icon=icon)
        ).add_to(m)

        folium.Circle(
            radius=50000,  # Radius in meters
            location=(lat, lon),
            color='red',
            fill=True,
            fill_opacity=0.1,
            weight=1
        ).add_to(m)

    for i in range(0, len(specific_points) - 1):
        folium.PolyLine(
            locations=[(specific_points[i][0], specific_points[i][1]), (specific_points[i+1][0], specific_points[i+1][1])],
            color="red",
            weight=1,
            dash_array="5, 5",
        ).add_to(m)
        folium.Circle(
            radius=50000,  # Radius in meters
            location=(lat, lon),
            color='red',
            fill=True,
            fill_opacity=0.1,
            weight=1
        ).add_to(m)

    for i in range(0, len(specific_points) - 1):
        folium.PolyLine(
            locations=[(specific_points[i][0], specific_points[i][1]), (specific_points[i+1][0], specific_points[i+1][1])],
            color="red",
            weight=1,
            dash_array="5, 5",
        ).add_to(m)


def main():
    """Main function to generate the map with grid and specific markers."""
    use_detailed_data = False
    position = get_position(use_detailed_data)
    """Main function to generate the map with grid and specific markers."""
    use_detailed_data = False
    position = get_position(use_detailed_data)

    lat_points, lon_points = calculate_grid_points(
        position.LAT_MIN, position.LAT_MAX, position.LON_MIN, position.LON_MAX, use_detailed_data
    )
    lat_points, lon_points = calculate_grid_points(
        position.LAT_MIN, position.LAT_MAX, position.LON_MIN, position.LON_MAX, use_detailed_data
    )

    map_center = [(position.LAT_MIN + position.LAT_MAX) / 2, (position.LON_MIN + position.LON_MAX) / 2]
    map_center = [(position.LAT_MIN + position.LAT_MAX) / 2, (position.LON_MIN + position.LON_MAX) / 2]
    m = initialize_map(map_center)

    add_grid_to_map(m, lat_points, lon_points, position)
    add_grid_to_map(m, lat_points, lon_points, position)
    add_markers_and_lines(m)

    m.save("gnss_quantique.html")
    print("The map with the grid and specific markers has been generated and saved as 'gnss_quantique.html'.")
    print("The map with the grid and specific markers has been generated and saved as 'gnss_quantique.html'.")


if __name__ == "__main__":
    main()