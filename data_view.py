import streamlit as st
import pandas as pd


st.title('ASAP')
st.subheader('Android Sensor Analysis Platform')

@st.cache_data
def get_accelerometer_df(input_df) -> pd.DataFrame:
  return input_df.set_index('sensor').filter(like='Accelerometer', axis=0)

uploaded_file = st.sidebar.file_uploader(
  "Choose a file",
  "csv"
)

if uploaded_file is not None:
  # data: sensor name, timestamp
  df = pd.read_csv(uploaded_file, names=['sensor','timestamp','value0','value1','value2','value3','value4','value5'])
  df['timestamp'] = pd.to_datetime(df['timestamp'],unit='ms')
  st.dataframe(df)

