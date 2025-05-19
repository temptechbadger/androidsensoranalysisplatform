import streamlit as st
import pandas as pd

# sidebar
sensor_data = st.sidebar.file_uploader(
  "Choose a file",
  "csv"
)

st.title('ASAP')
st.subheader('Analysis of the Light Sensor')

if sensor_data is not None:
  # data: sensor name, timestamp
  sdf = pd.read_csv(sensor_data,
                    names=['sensor','timestamp','light_level','value1','value2','value3','value4','value5','value6','value7','value8','value9','value10','value11','value12','value13','value14','value15'],
                    index_col='timestamp')
  # timezones tracked only as utc as of now
  sdf.index = pd.to_datetime(sdf.index, unit='ms', utc=True)
  sdf = sdf.drop(columns=['value1','value2','value3','value4','value5','value6','value7','value8','value9','value10','value11','value12','value13','value14','value15'])
  sdf = sdf[sdf['sensor'].str.endswith("Light Sensor")]
  st.write(f'{sdf.shape[0]} rows found')
  st.dataframe(sdf)
  st.line_chart(sdf, y='light_level')