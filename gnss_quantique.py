import folium
import numpy as np

# Coordonnées GPS avec certaines inconnues
lat_min = 42.000000
lat_max = 49.999999
lon_min = -5.000001
lon_max = 8.000001

# Nombre de points dans chaque direction
num_points = 2  # Augmenter pour plus de points

# Coordonnées du marqueur chez ré monde
specific_lat = 46.15878834400968
specific_lon = -1.2718925504584946

# Créer une grille de points
lat_points = np.linspace(lat_min, lat_max, num_points)
lon_points = np.linspace(lon_min, lon_max, num_points)

# Créer une carte centrée sur la zone
map_center = [(lat_min + lat_max) / 2, (lon_min + lon_max) / 2]

# Créer une carte centrée sur la zone avec un zoom initial réduit
m = folium.Map(location=map_center, zoom_start=6)

# Ajouter les points de la grille à la carte avec des étiquettes
for lat in lat_points:
    for lon in lon_points:
        folium.Marker(
            [lat, lon],
            popup=f"Lat: {lat:.4f}, Lon: {lon:.4f}",  # Étiquette pour chaque point
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(m)

# Ajouter les lignes de la grille à la carte avec des étiquettes pour les latitudes et longitudes
for lat in lat_points:
    folium.PolyLine([(lat, lon_min), (lat, lon_max)], color="blue", weight=1).add_to(m)
    # Ajouter une étiquette de latitude au milieu de chaque ligne horizontale, avec un décalage vers le haut
    mid_lon = (lon_min + lon_max) / 2
    folium.Marker(
        [lat, mid_lon],
        icon=folium.DivIcon(html=f'<div style="font-size: 12px; color: blue; margin-top: -10px;">Lat={lat:.6f}</div>')
    ).add_to(m)

for lon in lon_points:
    folium.PolyLine([(lat_min, lon), (lat_max, lon)], color="green", weight=1).add_to(m)
    # Ajouter une étiquette de longitude au milieu de chaque ligne verticale, avec le texte à la verticale et un décalage à gauche
    mid_lat = (lat_min + lat_max) / 2
    folium.Marker(
        [mid_lat, lon],
        icon=folium.DivIcon(html=f'<div style="font-size: 12px; color: green; transform: rotate(-90deg); margin-left: -10px;">Lon={lon:.6f}</div>')
    ).add_to(m)

# Ajouter le marqueur spécifique avec une étiquette rouge "1"
folium.Marker(
    [specific_lat, specific_lon],
    popup="enigme 1 chez Ré monde",
    icon=folium.Icon(color='red', icon='fa-solid fa-1')
).add_to(m)

# Sauvegarder la carte dans un fichier HTML
m.save("gnss_quantique.html")

print("La carte avec le quadrillage et le marqueur spécifique a été générée et sauvegardée dans 'gnss_quantique.html'.")
