import streamlit as st
import pandas as pd

# sidebar
sensor_data = st.sidebar.file_uploader(
  "Choose a file",
  "csv"
)

st.title('ASAP')
st.subheader('Analysis of the Accelerometer')

if sensor_data is not None:
  # data: sensor name, timestamp
  sdf = pd.read_csv(sensor_data,
                    names=['sensor','timestamp','x','y','z','value3','value4','value5','value6','value7','value8','value9','value10','value11','value12','value13','value14','value15'],
                    index_col='timestamp')
  # timezones tracked only as utc as of now
  sdf.index = pd.to_datetime(sdf.index, unit='ms', utc=True)
  sdf = sdf.drop(columns=['value3','value4','value5','value6','value7','value8','value9','value10','value11','value12','value13','value14','value15'])
  sdf = sdf[sdf['sensor'].str.endswith("Linear Acceleration Sensor")]
  # step: get time delta and compute speed difference over timeframe
  sdf['time'] = sdf.index
  sdf['time_delta'] = sdf['time'].shift(-1) - sdf['time']
  # total speed with the acceleraton over the timeframe
  sdf['delta_speed_x'] = sdf['x'] * sdf['time_delta'].dt.total_seconds() 
  sdf['delta_speed_y'] = sdf['y'] * sdf['time_delta'].dt.total_seconds()
  sdf['delta_speed_z'] = sdf['z'] * sdf['time_delta'].dt.total_seconds()
  # step: compute actual speed
  sdf['speed_x'] = sdf['delta_speed_x'].cumsum()
  sdf['speed_y'] = sdf['delta_speed_y'].cumsum()
  sdf['speed_z'] = sdf['delta_speed_z'].cumsum()

  st.write(f'{sdf.shape[0]} rows found')
  st.dataframe(sdf)
  st.write('In a perfect world, sum of the differences would be (0,0,0), to theoretically start and end at rest')
  st.write(f'Actual values are {sdf['delta_speed_x'].sum()}, {sdf['delta_speed_y'].sum()}, {sdf['delta_speed_z'].sum()}')
  st.line_chart(sdf, y=['x', 'y', 'z'])
