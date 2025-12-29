import glob, json

features = []

for file in glob.glob("activities/*.json"):
    with open(file) as f:
        coords = json.load(f)
        # Each run becomes a LineString feature
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": coords
            },
            "properties": {
                "id": file.split("/")[-1].replace(".json", "")
            }
        }
        features.append(feature)

geojson = {
    "type": "FeatureCollection",
    "features": features
}

with open("all_runs.geojson", "w") as f:
    json.dump(geojson, f)
