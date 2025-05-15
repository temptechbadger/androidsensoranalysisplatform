import streamlit as st
import pandas as pd
import requests
import numpy as np

from io import StringIO


# defining constants
PRESSURE_AT_SEA_LEVEL: float = 1013.25
MOLECULAR_MASS: float = 0.02896
GRAVITY: float = 0.9807
GAS_CONSTANT: float = 8.31446261815324
TEMPERATURE_LAPSE_RATE: float = -0.0065


# sidebar
sensor_data = st.sidebar.file_uploader(
  "Upload a sensor.csv file",
  "csv"
)
location_data = st.sidebar.file_uploader(
  "Upload a location.csv file",
  "csv"
)

has_sensor = sensor_data is not None and location_data is None
has_location = location_data is not None and sensor_data is None
has_both = sensor_data is not None and location_data is not None

assumed_temperature = 273 + st.sidebar.number_input('choose assumed temperature in °C', value=15)
st.sidebar.write("Gewählte Temperatur: ", assumed_temperature, "K")
pressure_difference_per_height: float = -((PRESSURE_AT_SEA_LEVEL*MOLECULAR_MASS*GRAVITY)/(GAS_CONSTANT*assumed_temperature))
resampling_enabled = st.sidebar.toggle("resample to seconds")


# data processing
if sensor_data is not None:
  # data: sensor name, timestamp
  sdf = pd.read_csv(sensor_data, names=['sensor','timestamp','value0','value1','value2','value3','value4','value5'])
  sdf['timestamp'] = pd.to_datetime(sdf['timestamp'],unit='ms')

  # specific step
  sdf = sdf.set_index('timestamp')
  sdf = sdf[sdf['sensor'] == "BMP380 Pressure Sensor"]
  # sdf = sdf[sdf['sensor'].endswith("Pressure Sensor")].set_index('timestamp').filter(like='Pressure Sensor', axis=0)
  sdf = sdf.drop(columns=['value1','value2','value3','value4','value5'])
  print(sdf)
  # if resampling_enabled:
  #   sdf = sdf.resample('s').agg({'sensor': 'first', 'value0': 'mean'})
  sdf['height'] = assumed_temperature/TEMPERATURE_LAPSE_RATE * (1-(sdf['value0']/1013.25)**(1/5.255))
  # 44330 = 288.145 / -0.0065 ( )


if location_data is not None:
  ldf = pd.read_csv(location_data, names=['timestamp', 'lat', 'lon'])
  ldf['timestamp'] = pd.to_datetime(ldf['timestamp'],unit='ms')
  # fourth decimal for coordinates correlates to 11.1m, thus the size
  url_request = str(ldf[['lat', 'lon']].values.tolist()).replace(' ','')
  #      https://www.elevation-api.eu/v1/elevation?pts=[[46.24566,6.17081],[46.85499,6.78134]] 
  url = "https://www.elevation-api.eu/v1/elevation?pts=%s" % (url_request)
  try:
    altitudes = pd.read_json(StringIO((requests.get(url)).text))
    ldf = pd.concat([ldf, altitudes], axis=1, names=['timestamp', 'lat', 'lon', 'height'])
  except ValueError:
    st.warning("too many coordinates commited at once")
  except:
    st.warning("unknown error occured")
  ldf = ldf.set_index('timestamp')
  # if resampling_enabled:
  #   ldf = ldf.resample('10s').mean()

if has_both:
  # print(ldf.set_index('timestamp'))
  print(ldf)
  print(sdf)
  # df = pd.concat([sdf, ldf])
  df = pd.concat([sdf, ldf]).sort_index()
  print(df)
  df['elevations'] = df['elevations'].interpolate()
  if resampling_enabled:
    agg_funcs = {
      'sensor': 'first',
      'value0': 'mean',
      'height': 'mean',
      'lat': 'mean',
      'lon': 'mean',
      'elevations': 'mean',
    }
    df = df.resample('s').agg(agg_funcs)

# form
st.title('ASAP')
st.subheader('Analysis of the Pressure Sensor')

if has_sensor:
  st.write('only sensor data given')
  st.write(f'{sdf.shape[0]} rows found')
  with st.expander('table of cleaned data here'):
    st.dataframe(sdf)
  st.line_chart(sdf, x=None, y=['height'])
  st.line_chart(sdf, x=None, y=['value0'])


if has_location:
  st.write('only location data given')
  with st.expander('show table'):
    st.dataframe(ldf)
  st.line_chart(ldf, y='elevations')
  st.map(ldf, size=11)

if has_both:
  st.write('both data available')
  with st.expander('table of cleaned data'):
    st.dataframe(df)
  st.line_chart(df, y=['height','elevations'])