print("Checking Pre-Requisites")
import pip

def import_or_install(package):
    try:
        __import__(package)
    except ImportError:
        pip.main(['install', package])

import_or_install('folium')

import folium
import pandas

data = pandas.read_csv('Volcanoes_USA.txt')

lat = data['LAT']
lon = data['LON']
elev = data['ELEV']

def color_prod(elevation):
	if elevation < 1000:
		return 'green'
	elif 1000<= elevation < 3000:
		return 'orange'
	else:
		return 'red'

map = folium.Map(location=[lat.mean(),lon.mean()], zoom_start=5, tiles='OpenStreetMap')

fgv = folium.FeatureGroup(name = 'Volcanoes')

for lt, lo, elev in zip(lat,lon,elev):
	fgv.add_child(folium.Marker(location=[lt,lo], popup=folium.Popup(str(elev), parse_html=True), icon = folium.Icon(color = color_prod(elev))))

fgp = folium.FeatureGroup(name = 'population')

fgp.add_child(folium.GeoJson(data= open('world.json','r',encoding='utf-8-sig').read(),
	style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000 else 'orange' 
	if 10000000<= x['properties']['POP2005'] < 20000000 else 'red'}))

map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl())

map.save("US_Maps_Volcanoes_And_Population.html")