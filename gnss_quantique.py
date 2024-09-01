import folium
import numpy as np
import math


class DetailedData:
    """Class representing the detailed search area."""
    LAT_MIN = 47.023456
    LAT_MAX = 47.923456
    LON_MIN = 6.023456
    LON_MAX = 6.923456


class SquareArea:
    """Class representing the broader square search area."""
    LAT_MIN = 42.000074
    LAT_MAX = 49.999974
    LON_MIN = 0.000000
    LON_MAX = 8.000000


def get_position(use_detailed_data):
    """Returns the position class based on the configuration."""
    return DetailedData() if use_detailed_data else SquareArea()


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


def calculate_points(diff_str):
    """Calculates the number of points based on the difference string."""
    points_list = [int(digit) + 1 for digit in diff_str if digit != '0']
    return max(math.prod(points_list), 1)


def initialize_map(center, zoom=6):
    """Initializes and returns a folium map centered at the given coordinates."""
    return folium.Map(location=center, zoom_start=zoom)


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
        folium.Marker(
            [lat, mid_lon],
            icon=folium.DivIcon(
                html=f'<div style="font-size: 12px; color: blue; margin-top: -10px;">Lat={lat:.6f}</div>')
        ).add_to(m)

    for lon in lon_points:
        folium.PolyLine([(position.LAT_MIN, lon), (position.LAT_MAX, lon)], color="green", weight=1).add_to(m)
        folium.Marker(
            [mid_lat, lon],
            icon=folium.DivIcon(
                html=f'<div style="font-size: 12px; color: green; transform: rotate(-90deg); margin-left: -10px;">Lon={lon:.6f}</div>')
        ).add_to(m)


def add_markers_and_lines(m):
    """Adds specific markers and lines between them to the map."""
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

        folium.Circle(
            radius=400000,  # Radius in meters
            location=(lat, lon),
            color='red',
            fill=True,
            fill_opacity=0,
            weight=1
        ).add_to(m)

    folium.PolyLine(
        locations=[(specific_points[0][0], specific_points[0][1]), (specific_points[1][0], specific_points[1][1])],
        color="red",
        weight=2,
    ).add_to(m)


def main():
    """Main function to generate the map with grid and specific markers."""
    use_detailed_data = False
    position = get_position(use_detailed_data)

    lat_points, lon_points = calculate_grid_points(
        position.LAT_MIN, position.LAT_MAX, position.LON_MIN, position.LON_MAX, use_detailed_data
    )

    map_center = [(position.LAT_MIN + position.LAT_MAX) / 2, (position.LON_MIN + position.LON_MAX) / 2]
    m = initialize_map(map_center)

    add_grid_to_map(m, lat_points, lon_points, position)
    add_markers_and_lines(m)

    m.save("gnss_quantique.html")
    print("The map with the grid and specific markers has been generated and saved as 'gnss_quantique.html'.")


if __name__ == "__main__":
    main()
