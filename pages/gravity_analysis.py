import streamlit as st
import pandas as pd

# sidebar
sensor_data = st.sidebar.file_uploader(
  "Choose a file",
  "csv"
)

st.title('ASAP')
st.subheader('Analysis of the gravity sensor')

if sensor_data is not None:
  sdf = pd.read_csv(sensor_data,
                    names=['sensor','timestamp','x','y','z','value3','value4','value5','value6','value7','value8','value9','value10','value11','value12','value13','value14','value15'],
                    index_col='timestamp')
  # timezones tracked only as utc as of now
  sdf.index = pd.to_datetime(sdf.index, unit='ms', utc=True)
  sdf = sdf.drop(columns=['value3','value4','value5','value6','value7','value8','value9','value10','value11','value12','value13','value14','value15'])
  sdf = sdf[sdf['sensor'].str.endswith("Gravity Sensor")]

  # sdf = sdf.resample('10s').agg({'sensor':'first', 'x': 'mean', 'y': 'mean', 'z': 'mean'})
  st.write(f'{sdf.shape[0]} rows found')
  with st.expander('show table'):
    st.dataframe(sdf)
  st.line_chart(sdf, y=['x', 'y', 'z'], color=["#080", "#00f", "#b22"])

# refer to the following graphic for rotation: https://developer.android.com/images/axis_device.png
  st.image('images/axis_device.png')
