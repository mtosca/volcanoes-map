import folium
import pandas as pd

# returns a color depending on the elevetion measure
def produce_elevation_color(elev):
    if elev < 1000:
        return 'green'
    if 1000 <= elev < 3000:
        return 'orange'
    return 'red'

# returns a color depending on the population count
def produce_population_color(pop):
    if pop < 10000000:
        return 'yellow'
    
    if 10000000 <= pop < 100000000:
        return 'orange'
    
    return 'red'

## load volcanoes data
volcanoes_data = pd.read_csv("volcanoes.csv")

# use lists cuz performance is better
latitudes = list(volcanoes_data["LAT"])
longitudes = list(volcanoes_data["LON"])
elevetions = list(volcanoes_data["ELEV"])


## start building map information
html = """<h4>Volcano information:</h4>
        Height: %s m
        """

# volcanoes position markers layer
fg_v = folium.FeatureGroup(name="Volcanoes locations")

# iterates 3 lists at the same time with the same index and three variables
for lat, lon, elev in zip(latitudes, longitudes, elevetions):
    iframe = folium.IFrame(html=html % str(elev), width=180, height=80)
    fg_v.add_child(folium.CircleMarker(location=(lat, lon), popup=folium.Popup(iframe), radius=7, fill_color=produce_elevation_color(elev), color='grey', fill_opacity=0.7))

## add population polygons layer (countries separation lines)
fg_p = folium.FeatureGroup(name="Population")
fg_p.add_child(folium.GeoJson(
    data=open("world.json", 'r', encoding='utf-8-sig').read(), 
    style_function=lambda x: {'fillColor': produce_population_color(x['properties']['POP2005'])})
)

# base map layer
map = folium.Map(location=(38.7767982,-100.8109970), zoom_start=5, tiles="Stamen Terrain")

# other layers as features
map.add_child(fg_v)
map.add_child(fg_p)

# add feature to enable and disable layers (features)
map.add_child(folium.LayerControl())

# save map to html map
map.save("map1.html")
