import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

# Load dataset day.csv dan hour.csv
day_df = pd.read_csv('../data/day.csv')
hour_df = pd.read_csv('../data/hour.csv')

# Convert 'dteday' to datetime format
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# Sidebar untuk filter rentang waktu
min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo
    st.image("https://th.bing.com/th/id/OIP.dzY5iX1-aq4Y1383yHoGrQAAAA?rs=1&pid=ImgDetMain")
    
    # Pilih rentang waktu
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter data berdasarkan rentang waktu
main_df = day_df[(day_df["dteday"] >= pd.to_datetime(start_date)) & 
                 (day_df["dteday"] <= pd.to_datetime(end_date))]

# Hitung total dan rata-rata peminjaman untuk hari kerja dan hari libur
total_weekday = main_df[main_df['workingday'] == 1]['cnt'].sum()
avg_weekday = main_df[main_df['workingday'] == 1]['cnt'].mean()

total_holiday = main_df[main_df['workingday'] == 0]['cnt'].sum()
avg_holiday = main_df[main_df['workingday'] == 0]['cnt'].mean()

# Dashboard Header
st.header('Bike Sharing Dashboard')

# Menampilkan informasi total dan rata-rata peminjaman
st.subheader("Statistik Peminjaman Sepeda")
col1, col2 = st.columns(2)

# Tampilan untuk hari kerja (weekday)
with col1:
    st.write("### Hari Kerja (Weekday)")
    st.metric(label="Total Peminjaman", value=total_weekday)
    st.metric(label="Rata-rata Peminjaman", value=f"{avg_weekday:.2f}")

# Tampilan untuk hari libur (holiday)
with col2:
    st.write("### Hari Libur (Holiday)")
    st.metric(label="Total Peminjaman", value=total_holiday)
    st.metric(label="Rata-rata Peminjaman", value=f"{avg_holiday:.2f}")

# Scatter plot: Suhu vs Total Peminjaman dengan Hari Kerja dan Libur
st.subheader("Pengaruh Suhu Terhadap Total Peminjaman Sepeda pada Hari Kerja vs Hari Libur")
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(data=day_df, x='temp', y='cnt', hue='workingday', palette='coolwarm', ax=ax)
ax.set_title('Pengaruh Suhu Terhadap Total Peminjaman Sepeda')
ax.set_xlabel('Suhu (Normalized)')
ax.set_ylabel('Jumlah Total Peminjaman Sepeda')
ax.legend(title='Hari Kerja')
st.pyplot(fig)

# Bar plot: Jumlah Peminjaman Pengguna Kasual Berdasarkan Kondisi Cuaca
st.subheader("Jumlah Peminjaman Pengguna Kasual Berdasarkan Kondisi Cuaca")

# Group by 'weathersit' and sum 'casual' rentals
weather_casual = day_df.groupby('weathersit')['casual'].sum()

# Create the plot
fig, ax = plt.subplots(figsize=(10, 6))
weather_casual.plot(kind='bar', color='skyblue', ax=ax)
ax.set_title('Jumlah Peminjaman Pengguna Kasual Berdasarkan Kondisi Cuaca')
ax.set_xlabel('Kondisi Cuaca')
ax.set_ylabel('Jumlah Peminjaman Pengguna Kasual')

# Set tick labels for weather categories
ax.set_xticks([0, 1, 2, 3])
ax.set_xticklabels(['Clear', 'Mist', 'Light Snow/Rain', 'Heavy Rain'], rotation=0)

st.pyplot(fig)

# Bar plot: Peminjaman Sepeda Pengguna Terdaftar vs Kasual per Jam
st.subheader("Peminjaman Sepeda Pengguna Terdaftar vs Kasual per Jam")

hourly_counts = hour_df.groupby('hr')[['casual', 'registered']].sum()

# Membuat bar plot perbandingan antara pengguna kasual dan terdaftar per jam
fig, ax = plt.subplots(figsize=(10, 6))
hourly_counts.plot(kind='bar', ax=ax)

# Menambahkan judul dan label pada plot
ax.set_title('Peminjaman Sepeda Pengguna Terdaftar vs Kasual per Jam')
ax.set_xlabel('Jam')
ax.set_ylabel('Jumlah Peminjaman')
ax.legend(['Kasual', 'Terdaftar'])

# Tampilkan plot menggunakan Streamlit
st.pyplot(fig)
