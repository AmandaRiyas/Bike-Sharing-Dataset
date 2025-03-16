import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Load data dari link
MNDday_df = pd.read_csv('https://raw.githubusercontent.com/AmandaRiyas/Bike-Sharing-Dataset/refs/heads/main/data/day.csv')

MNDday_df['dteday'] = pd.to_datetime(MNDday_df['dteday'])

# Agregasi data per bulan
monthly_rentals_df = MNDday_df.resample(rule='M', on='dteday').agg({
    "cnt": "sum",
    "weathersit": lambda x: stats.mode(x, keepdims=True)[0][0],
    "weekday": lambda x: stats.mode(x, keepdims=True)[0][0],
    "workingday": lambda x: stats.mode(x, keepdims=True)[0][0],
    "holiday": lambda x: stats.mode(x, keepdims=True)[0][0],
    "season": lambda x: stats.mode(x, keepdims=True)[0][0]
})
monthly_rentals_df.index = monthly_rentals_df.index.strftime('%Y-%m')
monthly_rentals_df = monthly_rentals_df.reset_index()
monthly_rentals_df.rename(columns={
    "dteday": "month",
    "cnt": "total_rentals"
}, inplace=True)

# Streamlit App
st.title("Bike Sharing Dashboard")
st.sidebar.header("Filter Data")

# Sidebar filters
selected_month = st.sidebar.selectbox("Pilih Bulan", monthly_rentals_df['month'].unique())

filtered_data = MNDday_df[MNDday_df['dteday'].dt.strftime('%Y-%m') == selected_month]

# Line Chart - Total Rentals Over Time
st.subheader("Total Penyewaan Sepeda Seiring Waktu")
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(filtered_data['dteday'], filtered_data['cnt'], marker='o', linestyle='-', color='b')
ax.set_xlabel("Tanggal")
ax.set_ylabel("Total Penyewa")
ax.set_title("Tren Penyewaan Sepeda")
st.pyplot(fig)

# Mapping kategori
category_labels = {
    "weathersit": {1: "Cerah", 2: "Berawan", 3: "Hujan/Salju Ringan"},
    "weekday": {0: "Minggu", 1: "Senin", 2: "Selasa", 3: "Rabu", 4: "Kamis", 5: "Jumat", 6: "Sabtu"},
    "workingday": {0: "Tidak", 1: "Ya"},
    "holiday": {0: "Tidak", 1: "Ya"},
    "season": {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
}

# Line Chart - Rentals by Category
st.subheader("Total Penyewaan Berdasarkan Kategori")
categories = ['weathersit', 'weekday', 'workingday', 'holiday', 'season']

fig, axes = plt.subplots(3, 2, figsize=(12, 12))
axes = axes.flatten()

for i, var in enumerate(categories):
    grouped_data = filtered_data.groupby(var)['cnt'].sum().reset_index()
    if var in category_labels:
        grouped_data[var] = grouped_data[var].replace(category_labels[var])
        all_categories = pd.DataFrame({var: list(category_labels[var].values())})
        grouped_data = pd.merge(all_categories, grouped_data, on=var, how='left').fillna(0)
    
    axes[i].plot(grouped_data[var], grouped_data['cnt'], marker='o', linestyle='-', color='green')
    axes[i].set_title(f"Total Penyewaan Berdasarkan {var.capitalize()}")
    axes[i].set_xlabel(var.capitalize())
    axes[i].set_ylabel("Total Penyewa")
    axes[i].tick_params(axis='x', rotation=15)

if len(categories) % 2 != 0:
    fig.delaxes(axes[-1])

plt.tight_layout()
st.pyplot(fig)

# Heatmap - Correlation Matrix
st.subheader("Heatmap Korelasi")
fig, ax = plt.subplots(figsize=(10, 6))
corr_matrix = filtered_data[['cnt', 'temp', 'atemp', 'hum', 'windspeed']].corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', linewidths=0.5, ax=ax)
st.pyplot(fig)

# Bar Chart - Rata-rata Penyewaan Berdasarkan Suhu
st.subheader("Rata-rata Penyewaan Berdasarkan Kategori Suhu")
filtered_data['atemp_label'] = pd.cut(filtered_data['atemp'], bins=[0, 0.3, 0.6, 1], labels=['Dingin', 'Sejuk', 'Panas'])
summary_atemp = filtered_data.groupby('atemp_label')['cnt'].mean().reset_index()

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(data=summary_atemp, x='atemp_label', y='cnt', palette='coolwarm', ax=ax)
ax.set_title("Rata-rata Penyewaan Berdasarkan Kategori Suhu")
ax.set_xlabel("Kategori Suhu")
ax.set_ylabel("Rata-rata Jumlah Penyewa")
plt.xticks(rotation=20)
plt.grid(axis="y", linestyle="--", alpha=0.7)
st.pyplot(fig)

# Kesimpulan
st.subheader("Kesimpulan")
st.write("- Dari seluruh proses analisis data yang telah dilakukan kita dapat disimpulkan bahwa pola penyewaan sepeda berdasarkan kondisi cuaca, weekday, workingday, holiday, dan season yaitu penyewa sepeda tertinggi terjadi ketika workingday (tidak dalam masa holiday) terutama pada hari Jumat ketika cuaca cerah di musim gugur (Fall). Penyewaan sepeda terendah terjadi ketika bukan workingday (holiday) terutama hari Minggu ketika cuaca hujan/salju ringan di musim gugur (Fall).")
st.write("- Dari seluruh proses analisis data yang telah dilakukan kita dapat disimpulkan bahwa pengaruh dari atemp, hum, windspeed terhadap banyaknya penyewa sepeda yaitu atemp memiliki pengaruh yang kuat terhadap jumlah penyewa sepeda, semakin tinggi atemp maka semakin tinggi pula jumlah penyewa sepeda. Windspeed hanya memiliki korelasi lemah dan negatif, artinya setiap windspeed meningkat akan sedikit menurunkan jumlah penyewa sepeda, dan kelembaban (hum) tidak memiliki korelasi dengan jumlah penyewa sepeda.")
