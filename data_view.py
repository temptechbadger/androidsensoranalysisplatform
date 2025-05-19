import streamlit as st
import pandas as pd

st.title('ASAP')
st.subheader('Android Sensor Analysis Platform')

sensor_data = st.sidebar.file_uploader(
  "Upload a sensor.csv file",
  "csv"
)

location_data = st.sidebar.file_uploader(
  "Upload a location.csv file",
  "csv"
)

if sensor_data is not None:
  # data: sensor name, timestamp
  sdf = pd.read_csv(sensor_data,
                    names=['sensor','timestamp','value0','value1','value2','value3','value4','value5','value6','value7','value8','value9','value10','value11','value12','value13','value14','value15'],
                    index_col='timestamp')
  sdf.index = pd.to_datetime(sdf.index,unit='ms')
  st.dataframe(sdf)

  sensors_df = sdf.sensor.unique()
  st.dataframe(sensors_df)

if location_data is not None:
  ldf = pd.read_csv(location_data, names=['timestamp', 'latitude', 'longitude'])
  ldf['timestamp'] = pd.to_datetime(ldf['timestamp'],unit='ms')
  st.dataframe(ldf)
  # fourth decimal for coordinates is tracked and correlates to 11.1m, thus the size
  st.map(ldf, size=11)
