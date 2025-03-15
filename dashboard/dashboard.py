import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset from GitHub URL
url = "https://raw.githubusercontent.com/AmandaRiyas/Bike-Sharing-Dataset/refs/heads/main/data/day.csv"
df = pd.read_csv(url)

df['dteday'] = pd.to_datetime(df['dteday'])  # Convert to datetime

# Streamlit App
st.title("Bike Sharing Dashboard")
st.sidebar.header("Filter Data")

# Sidebar filters
selected_year = st.sidebar.selectbox("Select Year", df['yr'].unique(), format_func=lambda x: f"{2011 + x}")

df_filtered = df[df['yr'] == selected_year]

# Line Chart - Rentals Over Time
st.subheader("Total Bike Rentals Over Time")
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(df_filtered['dteday'], df_filtered['cnt'], marker='o', linestyle='-', color='b')
ax.set_xlabel("Date")
ax.set_ylabel("Total Rentals")
ax.set_title("Bike Rentals Trend")
st.pyplot(fig)

# Line Chart - Rentals by Category
st.subheader("Total Rentals by Category")
categories = ['weathersit', 'weekday', 'workingday', 'holiday', 'season']
selected_category = st.selectbox("Select Category", categories)

grouped_data = df_filtered.groupby(selected_category)['cnt'].sum().reset_index()
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(grouped_data[selected_category], grouped_data['cnt'], marker='o', linestyle='-', color='g')
ax.set_xlabel(selected_category.capitalize())
ax.set_ylabel("Total Rentals")
ax.set_title(f"Total Rentals by {selected_category.capitalize()}")
st.pyplot(fig)

# Heatmap - Correlation Matrix
st.subheader("Correlation Heatmap")
fig, ax = plt.subplots(figsize=(10, 6))
corr_matrix = df_filtered[['cnt', 'temp', 'atemp', 'hum', 'windspeed']].corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', linewidths=0.5, ax=ax)
st.pyplot(fig)

# Conclusion Section
st.subheader("Kesimpulan")
st.write("- Dari seluruh proses analisis data yang telah dilakukan kita dapat disimpulkan bahwa pola penyewaan sepeda berdasarkan kondisi cuaca, weekday, workingday, holiday, dan season yaitu penyewa sepeda tertinggi terjadi ketika workingday (tidak dalam masa holiday) terutama pada hari Jumat ketika cuaca cerah di musim gugur (Fall). Penyewaan sepeda terendah terjadi ketika bukan workingday (holiday) terutama hari Minggu ketika cuaca hujan/salju ringan di musim gugur (Fall).")
st.write("- Dari seluruh proses analisis data yang telah dilakukan kita dapat disimpulkan bahwa pengaruh dari atempt, hum, windspeed terhadap banyaknya penyewa sepeda yaitu atemp memiliki pengaruh yang kuat terhadap jumlah penyewa sepeda, semakin tinggi atemp maka semakin tinggi pula jumlah penyewa sepeda. Windspeed hanya memiliki korelasi lemah dan negatif, artinya setiap windspeed meningkat akan sedikit menurunkan jumlah penyewa sepeda, dan kelembaban (hum) tidak memiliki korelasi dengan jumlah penyewa sepeda.")
