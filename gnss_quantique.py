import folium
import numpy as np
import math
import json
from shapely.geometry import Point, shape


class DetailedData:
    """Class representing the detailed search area."""
    LAT_MIN = 45.027884
    LAT_MAX = 49.927884
    LON_MIN = 0.086674
    LON_MAX = 8.986674


class SquareArea:
    """Class representing the broader square search area."""
    LAT_MIN = 47.027884
    LAT_MAX = 49.927884
    LON_MIN = 0.086674
    LON_MAX = 8.086674


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
    print(f"num_points_lat: {num_points_lat}\tnum_points_lon: {num_points_lon}")
    return np.linspace(lat_min, lat_max, num_points_lat), np.linspace(lon_min, lon_max, num_points_lon)


def calculate_diffs(lat_min, lat_max, lon_min, lon_max):
    """Calculates differences in latitude and longitude as strings of microdegrees."""
    lat_diff_micro = int(round((lat_max - lat_min) * 1e6))

    if lon_min < 0:
        lon_diff_micro = int(round((lon_max - abs(lon_min)) * 1e6))
    else:
        lon_diff_micro = int(round((lon_max - lon_min) * 1e6))
    print(f"lat_diff_micro: {lat_diff_micro}\tlon_diff_micro: {lon_diff_micro}")
    return str(lat_diff_micro), str(lon_diff_micro)


def calculate_points(diff_str):
    """Calculates the number of points based on the difference string."""
    points_list = [int(digit) + 1 for digit in diff_str if digit != '0']
    print(f"diff_str={diff_str}\tpoints_list={points_list}")
    return max(math.prod(points_list), 1)


def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculates the great-circle distance between two points on the Earth using the Haversine formula."""
    R = 6371  # Radius of the Earth in kilometers
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))

    return R * c  # Distance in kilometers


def initialize_map(center, zoom=6):
    """Initializes and returns a folium map centered at the given coordinates."""
    return folium.Map(location=center, zoom_start=zoom)


def add_grid_to_map(m, lat_points, lon_points, position, specific_points, radius, geojson_polygons, grid):
    """Adds grid points and lines to the map, excluding those within a radius of specific points and ensuring it is inside all geojson polygons."""
    mid_lon = (position.LON_MIN + position.LON_MAX) / 2
    mid_lat = (position.LAT_MIN + position.LAT_MAX) / 2

    for lat in lat_points:
        for lon in lon_points:
            # Check if the current point is within the radius of any specific points
            within_radius = False
            for spec_lat, spec_lon, _, _ in specific_points:
                if haversine_distance(lat, lon, spec_lat, spec_lon) < radius / 1e3:
                    within_radius = True
                    break


            point = Point(lon, lat)
            # Check if the current point is inside any of the GeoJSON polygons
            inside_list = []
            for geojson in geojson_polygons:
                inside_geojson = any(polygon.contains(point) for polygon in geojson)
                if inside_geojson:
                    inside_list.append(True)

            inside = True if len(inside_list) == len(geojson_polygons) else False

            if within_radius or not inside:
                continue  # Skip this point if it falls within the radius or is not inside all polygons

            # Add grid point marker
            folium.Marker(
                [lat, lon],
                popup=f"Lat: {lat:.6f}, Lon: {lon:.6f}",
                icon=folium.Icon(color="blue", icon="info-sign")
            ).add_to(m)

        if grid:
            # Add latitude grid line
            folium.PolyLine([(lat, position.LON_MIN), (lat, position.LON_MAX)], color="blue", weight=1).add_to(m)
            folium.Marker(
                [lat, mid_lon],
                icon=folium.DivIcon(
                    html=f'<div style="font-size: 12px; color: blue; margin-top: -10px;">Lat={lat:.6f}</div>')
            ).add_to(m)

            for lon in lon_points:
                # Add longitude grid line
                folium.PolyLine([(position.LAT_MIN, lon), (position.LAT_MAX, lon)], color="green", weight=1).add_to(m)
                folium.Marker(
                    [mid_lat, lon],
                    icon=folium.DivIcon(
                        html=f'<div style="font-size: 12px; color: green; transform: rotate(-90deg); margin-left: -10px;">Lon={lon:.6f}</div>')
                ).add_to(m)


def add_markers_and_lines(m, radius):
    """Adds specific markers and lines between them to the map."""
    specific_points = [
        (46.15878834400968, -1.2718925504584946, "Enigme 1 chez Ré monde", 'fa-solid fa-1'),
        (50.721787866105565, 2.5337913136757573, "Enigme 2 les 3 Citrouilles", 'fa-solid fa-2'),
        (47.47327153775195, -0.5550084763123877, "Enigme 3 La Glacerie d'Anjou", 'fa-solid fa-3'),
        (46.141782734484735, 1.879348485208694, "Enigme 4 La Pierre Mystere", 'fa-solid fa-4'),
        (43.61277522184278, 3.879513380408009, "Enigme 5 AlphaNef", 'fa-solid fa-5'),
        (49.67185797928755, 4.842056015264417, "Enigme 6 Chapelle Saint-Roger", 'fa-solid fa-6'),
        (43.12303479835759, 1.6946271347407884, "Enigme 7 Librairie Le Bleu du Ciel", 'fa-solid fa-7'),
        (47.35711347592077, 4.9650404744590455, "Enigme 8 La Porte du Diable", 'fa-solid fa-8'),
        (48.51271190767063, 7.164272246565264, "Enigme 9 Temple du Donon", 'fa-solid fa-9'),
        (48.4148436, 2.6454519, "Enigme 10 Fontainebleau", 'fa-solid fa-a'),
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
            radius=radius,  # Radius in meters
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

    return specific_points


def add_geojson_to_map(m, geojson_file_path):
    """Loads a GeoJSON file and adds it to the map."""
    with open(geojson_file_path) as f:
        geojson_data = json.load(f)
    folium.GeoJson(
        geojson_data,
        name="geojson"
    ).add_to(m)


def load_geojson_polygons(geojson_file_paths):
    """Loads multiple GeoJSON files and returns a list of Shapely polygons."""
    if len(geojson_file_paths) != 0:
        geojson_list = []

        for geojson_file_path in geojson_file_paths:
            polygons = []
            with open(geojson_file_path) as f:
                geojson_data = json.load(f)

            for feature in geojson_data['features']:
                polygons.append(shape(feature['geometry']))  # Convert the geometry into Shapely polygon

            geojson_list.append(polygons)
        return geojson_list
    else:
        return False


def main():
    """Main function to generate the map with grid and specific markers."""
    use_detailed_data = True
    radius_m = 50000
    grid = False
    position = get_position(use_detailed_data)

    lat_points, lon_points = calculate_grid_points(
        position.LAT_MIN, position.LAT_MAX, position.LON_MIN, position.LON_MAX, use_detailed_data
    )

    map_center = [(position.LAT_MIN + position.LAT_MAX) / 2, (position.LON_MIN + position.LON_MAX) / 2]
    m = initialize_map(map_center)

    # Get the specific points to check for exclusion
    specific_points = add_markers_and_lines(m, radius_m)

    # Add GeoJSON files
    geojson_file_paths = ['./maps/myrtilles.geojson', './maps/forets_mixtes.geojson', './maps/sapins.geojson']
    geojson_polygons = load_geojson_polygons(geojson_file_paths)

    # Add grid points excluding those that fall within a 50 km radius of specific points and are inside all GeoJSON polygons
    add_grid_to_map(m, lat_points, lon_points, position, specific_points, radius_m, geojson_polygons, grid)

    m.save("gnss_quantique.html")
    print("The map with the filtered grid and specific markers has been generated and saved as 'gnss_quantique.html'.")

if __name__ == "__main__":
    main()
