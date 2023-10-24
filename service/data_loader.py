import pandas as pd
import h3, json

# def convert_to_h3(coordinates):
#     lat, lon = coordinates[1], coordinates[0]
#     h3_hex = h3.geo_to_h3(lat, lon, resolution=11)
#     return h3_hex

def load_data():
	df = pd.read_csv('data/apartments.csv')
	df[['lat', 'lon']] = df['geopos'].str.extract(r'(\d+\.\d+), (\d+\.\d+)')
	df['lat'] = df['lat'].astype(float)
	df['lon'] = df['lon'].astype(float)
	df['h3_hex'] = df.apply(axis=1, func=lambda x: h3.geo_to_h3(x['lon'], x['lat'], resolution=11))

	return df
