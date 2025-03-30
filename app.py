import streamlit as st
import pandas as pd

st.title('ASAP')
st.subheader('Android Sensor Analysis Platform')

@st.cache_data
def get_accelerometer_df(input_df) -> pd.DataFrame:
  return input_df.set_index('sensor').filter(like='Accelerometer', axis=0)

@st.cache_data
def get_pressure_df(input_df) -> pd.DataFrame:
  return input_df.set_index('sensor').filter(like='Pressure Sensor', axis=0)

uploaded_file = st.sidebar.file_uploader(
  "Choose a file",
  "csv"
)

# Add a slider to the sidebar:
add_slider = st.sidebar.slider(
    'Limit accuracy',
    0, 12, 12
)

if uploaded_file is not None:
  # data: sensor name, timestamp
  df = pd.read_csv(uploaded_file, names=['sensor','timestamp','value0','value1','value2','value3','value4','value5'])
  df['timestamp'] = pd.to_datetime(df['timestamp'],unit='ms')
  st.dataframe(df)
  df_pres = get_pressure_df(df)
  print(df_pres.shape)
  st.line_chart(df_pres, x='timestamp', y='value0')

