import json

from flask import Flask
import folium

app = Flask(__name__)

@app.route('/')
def index():
    city_map = folium.Map(location=[56.3287, 44.0020], zoom_start=12)

    with open("places.json", 'r', encoding="utf-8") as f:
        places_data = json.load(f)

    markers = {}

    for _ in places_data:
        category = _["category"]

        if category not in markers:
            markers[category] = folium.FeatureGroup(name=category)
            city_map.add_child(markers[category])

    for place in places_data:
        folium.Marker(
            location=[place['latitude'], place['longitude']],
            popup=f"<b>{place['name']}</b><br>{place['description']}",
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(markers[place["category"]])



    dark_them = folium.TileLayer('cartodbdark_matter', name="Темная тема")
    satellite_layer = folium.TileLayer('https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', max_zoom=20, name='Спутник', attr='Map data © Google')
    hybrid_layer = folium.TileLayer('https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', max_zoom=20, name='Гибрид', attr='Map data © Google')


    city_map.add_child(dark_them)
    city_map.add_child(satellite_layer)
    city_map.add_child(hybrid_layer)

    folium.LayerControl().add_to(city_map)

    map_html = city_map.get_root().render()

    return map_html

if __name__ == '__main__':
    app.run(debug=True)
