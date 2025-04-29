import streamlit as st
import pandas as pd

# sidebar
uploaded_file = st.sidebar.file_uploader(
  "Choose a file",
  "csv"
)

st.title('ASAP')
st.subheader('Analysis of the Accelerometer')

if uploaded_file is not None:
  # data: sensor name, timestamp
  df = pd.read_csv(uploaded_file, names=['sensor','timestamp','value0','value1','value2','value3','value4','value5'])
  df['timestamp'] = pd.to_datetime(df['timestamp'],unit='ms')
  # specific step
  df = df.set_index('sensor').filter(like='Accelerometer', axis=0)
  df = df.drop(columns=['value3','value4','value5'])

#   df = df.resample('10s', on='timestamp').sum()
  st.write(f'{df.shape[0]} rows found')
  st.dataframe(df)
  st.line_chart(df, x='timestamp', y=['value0', 'value1', 'value2'])
  
st.subheader('Analysis of the linear acceleration')
if uploaded_file is not None:
  # data: sensor name, timestamp
  df_linear = pd.read_csv(uploaded_file, names=['sensor','timestamp','value0','value1','value2','value3','value4','value5'])
  df_linear['timestamp'] = pd.to_datetime(df['timestamp'],unit='ms')
  # specific step
  df_linear = df_linear.set_index('sensor').filter(like='Linear Acceleration', axis=0)
  df_linear = df_linear.drop(columns=['value3','value4','value5'])
  df_linear['time_delta'] = df_linear.timestamp.diff()

#   df = df.resample('10s', on='timestamp').sum()
  st.write(f'{df_linear.shape[0]} rows found')
  st.dataframe(df_linear)
  st.line_chart(df_linear, x='timestamp', y=['value0', 'value1', 'value2'])

# solution to time delta problem:
# https://codereview.stackexchange.com/questions/210070/calculating-time-deltas-between-rows-in-a-pandas-dataframe
#     x['time_delta'] = x['timestamp'] - x['timestamp'].shift()
# better -> x['time_delta'] = x.timestamp.diff()