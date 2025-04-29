import streamlit as st
import pandas as pd

# sidebar
uploaded_file = st.sidebar.file_uploader(
  "Choose a file",
  "csv"
)

st.title('ASAP')
st.subheader('Analysis of the Accelerometer, Magnetometer and Rotation?')

if uploaded_file is not None:
  # data: sensor name, timestamp
  df = pd.read_csv(uploaded_file, names=['sensor','timestamp','value0','value1','value2','value3','value4','value5'])
  df['timestamp'] = pd.to_datetime(df['timestamp'],unit='ms')
  # specific step
  st.write(f'{df.shape[0]} rows found')
  
  # LIS2MDL Magnetometer,1742634288855,-42.7, 16.875, 1.8875

  # Rotation Vector Sensor,1742634288897,0.038333483, -0.73399866, 0.09602183, 0.671235, 1.0471976
  # unit quaternion

# MISTRAL GENERATED ANSWER, CAUTION
#    Um den Quaternion den Gerätedrehwinkel und die Richtung Norden zu bestimmen, müssen Sie die Quaternion-Werte
# umwandeln in eine Rotationsmatrix und anschließend auf diese Matrix die Euler-Angel-Rotation berechnen. Der Winkel
# der Euler-Angel-Rotation um die Y-Achse entspricht der Gerätedrehung (Pitch) und weist dabei zur Richtung Norden.

# Hier eine Methode in Python, wie dies geschieht:

# ```python
# import numpy as np

# quaternion = [cos(θ/2), x*sin(θ/2), y*sin(θ/2), z*sin(θ/2)]  # Assuming quaternion is passed as a list.

# # Convert Quaternion to Rotation Matrix (Rotation matrix representation of the quaternion)
# R = np.array([[
#     1-2*(y**2 + z**2),  2*(x*y - z*w),   2*(x*z + y*w),
#     2*(x*y + z*w),      1-2*(x**2 + z**2), 2*(y*z - x*w),
#     2*(x*z - y*w),       2*(y*z + x*w),   1-2*(x**2 + y**2)
# ])

# # Rotation matrix to Euler Angles (Yaw, Pitch, Roll) using Rodrigues' rotation formula
# [roll, pitch, yaw] = np.rad2deg(np.array([
#     np.arctan2(R[0, 2], R[2, 2]),  # Pitch (Northern Angle)
#     np.arcsin(-R[1, 0]),             # Yaw (Heading Angle)
#     np.arctan2(R[0, 1], R[0, 0])      # Roll
# ]))
# ```

# Im erwähnten Code wird der Winkel um die Y-Achse (Pitch) berechnet, indem der zweite Eintrag der Rotationsmatrix
# verwendet wird (d.h., `R[1, 0]`). Dieser Winkel gibt an, wie weit das Gerät sich gegenüber der Richtung Norden
# gedreht ist und kann als Gerätedrehung interpretiert werden.

# Die genaue Umwandlung von Quaternion zu Rotationsmatrix (Rotation matrix representation of the quaternion) beruht
# auf der Formel:

# ```
# R = [1-2*(y^2 + z^2), 2*(x*y - z*w), 2*(x*z + y*w),
#     2*(x*y + z*w),      1-2*(x^2 + z^2), 2*(y*z - x*w),
#     2*(x*z - y*w),       2*(y*z + x*w),   1-2*(x^2 + y^2)]
# ```