import json
import folium
from folium.plugins import HeatMap

# Load your combined dataset
with open("all_runs.geojson") as f:
    data = json.load(f)

# Extract all GPS points from every run
points = []
for feature in data["features"]:
    coords = feature["geometry"]["coordinates"]
    points.extend(coords)

# Center the map roughly on Brushy Creek, TX
m = folium.Map(location=[30.5, -97.7], zoom_start=12)

# Add heatmap layer
HeatMap(points, radius=6, blur=4).add_to(m)

# Save to HTML file
m.save("heatmap.html")

print("Heatmap saved to heatmap.html")
