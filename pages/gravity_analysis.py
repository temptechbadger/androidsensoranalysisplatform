import streamlit as st
import pandas as pd

# sidebar
uploaded_file = st.sidebar.file_uploader(
  "Choose a file",
  "csv"
)

st.title('ASAP')
st.subheader('Analysis of the gravity sensor')

if uploaded_file is not None:
  # data: sensor name, timestamp
  df = pd.read_csv(uploaded_file, names=['sensor','timestamp','x','y','z','value3','value4','value5'])
  df['timestamp'] = pd.to_datetime(df['timestamp'],unit='ms')
  # specific step
  # df = df.set_index('sensor').filter(like='Gravity Sensor', axis=0)
  df = df.set_index('timestamp')
  df = df[df['sensor'] == "Gravity Sensor"]

  df = df.drop(columns=['value3','value4','value5'])

#   df = df.resample('10s', on='timestamp').sum()
  st.write(f'{df.shape[0]} rows found')
  with st.expander('show table'):
    st.dataframe(df)
  st.line_chart(df, y=['x', 'y', 'z'])

# refer to the following graphic for rotation: https://developer.android.com/images/axis_device.png
  st.image('images/axis_device.png')
