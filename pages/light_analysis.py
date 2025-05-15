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
  df = pd.read_csv(sensor_data, names=['sensor','timestamp','value0','value1','value2','value3','value4','value5','value6','value7','value8','value9','value10','value11','value12','value13','value14','value15'])
  df['timestamp'] = pd.to_datetime(df['timestamp'],unit='ms')
  # specific step
  df = df.set_index('sensor').filter(like='Light Sensor', axis=0)
  df = df[['timestamp','value0']]
  st.write(f'{df.shape[0]} rows found')
  st.dataframe(df)
  st.line_chart(df, x='timestamp', y='value0')