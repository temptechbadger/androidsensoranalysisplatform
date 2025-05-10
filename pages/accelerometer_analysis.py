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
  # step: single out sensor and needed values
  df = df.set_index('sensor').filter(like='Linear Acceleration', axis=0)
  df = df.drop(columns=['value3','value4','value5'])
  # step: get time delta and compute speed difference over timeframe
  df['time_delta'] = df['timestamp'].shift(-1) - df['timestamp']
  # total speed with the acceleraton over the timeframe
  df['delta_speed_x'] = df['value0'] * df['time_delta'].dt.total_seconds() 
  df['delta_speed_y'] = df['value1'] * df['time_delta'].dt.total_seconds()
  df['delta_speed_z'] = df['value2'] * df['time_delta'].dt.total_seconds()
  # step: compute actual speed
  # doesn't work, doesn't use the previous calculated value but always 0. Gotta fix.
  # for index, row in df.iterrows():
  #   row['speed_x'] = row['delta_speed_x'] - df.iloc[[index-1]].speed_x
  #   row['speed_y'] = row['delta_speed_y'] - df.iloc[[index-1]].speed_y
  #   row['speed_z'] = row['delta_speed_z'] - df.iloc[[index-1]].speed_z
  df['speed_x'] = df['delta_speed_x'].cumsum()
  df['speed_y'] = df['delta_speed_y'].cumsum()
  df['speed_z'] = df['delta_speed_z'].cumsum()

#   df = df.resample('10s', on='timestamp').sum()
  st.write(f'{df.shape[0]} rows found')
  st.dataframe(df)
  st.write('In a perfect world, sum of the differences would be (0,0,0), to start and end at 0 speed')
  st.write(f'Actual values are {df['delta_speed_x'].sum()}, {df['delta_speed_y'].sum()}, {df['delta_speed_z'].sum()}')
  st.line_chart(df, x='timestamp', y=['value0', 'value1', 'value2'])