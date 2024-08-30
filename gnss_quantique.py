import folium
import numpy as np

# hypothese pour accurate details_data
# lat_min = 47.120456
# lat_max = 47.129456
# lon_min = 6.123456
# lon_max = 6.123456

# square search area
lat_min = 42.000074
lat_max = 49.999974
lon_min = -5.000000
lon_max = 8.000000

# Toggle detailed grid calculation
details_data = False

if details_data:
    # Calculate the differences between latitudes and longitudes
    lat_diff = lat_max - lat_min
    lon_diff = lon_max - lon_min

    # Calculate the number of grid points based on non-zero digits in the differences
    num_points_lat = sum(int(digit) + 1 for digit in str(int(lat_diff * 10 ** 6)) if digit != '0')
    num_points_lon = sum(int(digit) + 1 for digit in str(int(lon_diff * 10 ** 6)) if digit != '0')

    # Ensure at least one point is calculated
    num_points_lon = max(num_points_lon, 1)
else:
    # Default to a simple 2x2 grid if details are not needed
    num_points_lat = 2
    num_points_lon = 2

print(f"Number of latitude points: {num_points_lat}")
print(f"Number of longitude points: {num_points_lon}")

# Generate latitude and longitude points for the grid
lat_points = np.linspace(lat_min, lat_max, num_points_lat)
lon_points = np.linspace(lon_min, lon_max, num_points_lon)

# Calculate the center of the map for initialization
map_center = [(lat_min + lat_max) / 2, (lon_min + lon_max) / 2]

# Initialize the map centered on the area with a starting zoom level
m = folium.Map(location=map_center, zoom_start=6)

# Add grid points to the map with labels
for lat in lat_points:
    for lon in lon_points:
        folium.Marker(
            [lat, lon],
            popup=f"Lat: {lat:.6f}, Lon: {lon:.6f}",
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(m)

# Add horizontal grid lines with latitude labels
mid_lon = (lon_min + lon_max) / 2
for lat in lat_points:
    folium.PolyLine([(lat, lon_min), (lat, lon_max)], color="blue", weight=1).add_to(m)
    folium.Marker(
        [lat, mid_lon],
        icon=folium.DivIcon(html=f'<div style="font-size: 12px; color: blue; margin-top: -10px;">Lat={lat:.6f}</div>')
    ).add_to(m)

# Add vertical grid lines with longitude labels
mid_lat = (lat_min + lat_max) / 2
for lon in lon_points:
    folium.PolyLine([(lat_min, lon), (lat_max, lon)], color="green", weight=1).add_to(m)
    folium.Marker(
        [mid_lat, lon],
        icon=folium.DivIcon(
            html=f'<div style="font-size: 12px; color: green; transform: rotate(-90deg); margin-left: -10px;">Lon={lon:.6f}</div>')
    ).add_to(m)

# Add the first specific marker with a custom label
specific_lat_1 = 46.15878834400968
specific_lon_1 = -1.2718925504584946
folium.Marker(
    [specific_lat_1, specific_lon_1],
    popup="Enigme 1 chez Ré monde",
    icon=folium.Icon(color='red', icon='fa-solid fa-1')
).add_to(m)

# Add the second specific marker with a custom label
specific_lat_2 = 50.721787866105565
specific_lon_2 = 2.5337913136757573
folium.Marker(
    [specific_lat_2, specific_lon_2],
    popup="Enigme 2 les 3 Citrouilles",
    icon=folium.Icon(color='red', icon='fa-solid fa-2')
).add_to(m)

# Draw a red line between the two markers
folium.PolyLine(
    locations=[[specific_lat_1, specific_lon_1], [specific_lat_2, specific_lon_2]],
    color="red",
    weight=2,  # Line thickness
).add_to(m)

# Save the map to an HTML file
m.save("gnss_quantique.html")

print("The map with the grid and specific marker has been generated and saved as 'gnss_quantique.html'.")
