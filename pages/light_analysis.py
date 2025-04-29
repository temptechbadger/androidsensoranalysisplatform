import streamlit as st
import pandas as pd

# sidebar
uploaded_file = st.sidebar.file_uploader(
  "Choose a file",
  "csv"
)

st.title('ASAP')
st.subheader('Analysis of the Light Sensor')

if uploaded_file is not None:
  # data: sensor name, timestamp
  df = pd.read_csv(uploaded_file, names=['sensor','timestamp','value0','value1','value2','value3','value4','value5'])
  df['timestamp'] = pd.to_datetime(df['timestamp'],unit='ms')
  # specific step
  df = df.set_index('sensor').filter(like='Light Sensor', axis=0)
  df = df.drop(columns=['value1','value2','value3','value4','value5'])
  st.write(f'{df.shape[0]} rows found')
  st.dataframe(df)
  st.line_chart(df, x='timestamp', y='value0')