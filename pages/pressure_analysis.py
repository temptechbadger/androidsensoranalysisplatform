import streamlit as st
import pandas as pd

# defining constants
PRESSURE_AT_SEA_LEVEL: float = 1013.25
MOLECULAR_MASS: float = 0.02896
GRAVITY: float = 0.9807
GAS_CONSTANT: float = 8.31446261815324
TEMPERATURE_LAPSE_RATE: float = -0.0065

# sidebar
uploaded_file = st.sidebar.file_uploader(
  "Choose a file",
  "csv"
)
assumed_temperature = 273 + st.sidebar.number_input('choose assumed temperature in °C', value=15)
st.sidebar.write("Gewählte Temperatur: ", assumed_temperature, "K")
pressure_difference_per_height: float = -((PRESSURE_AT_SEA_LEVEL*MOLECULAR_MASS*GRAVITY)/(GAS_CONSTANT*assumed_temperature))

st.title('ASAP')
st.subheader('Analysis of the Pressure Sensor')

if uploaded_file is not None:
  # data: sensor name, timestamp
  df = pd.read_csv(uploaded_file, names=['sensor','timestamp','value0','value1','value2','value3','value4','value5'])
  df['timestamp'] = pd.to_datetime(df['timestamp'],unit='ms')

  # specific step
  df = df.set_index('sensor').filter(like='Pressure Sensor', axis=0)
  df = df.drop(columns=['value1','value2','value3','value4','value5'])
  df = df.resample('s', on='timestamp').mean()
  df['height'] = assumed_temperature/-TEMPERATURE_LAPSE_RATE * (1-(df['value0']/1013.25)**(1/5.255))
  # 44330 * 0.0065 = 288.145 ( )

  # results
  st.write(f'{df.shape[0]} rows found')
  st.dataframe(df)
  st.line_chart(df, y=['height'])

  # conclusion:
  # consistent sensor activity needs a revisit
  # data unreliable indoors (houses, vehicles, especially planes)