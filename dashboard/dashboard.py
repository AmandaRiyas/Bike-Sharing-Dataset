import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Load data dari link
MNDday_df = pd.read_csv('https://raw.githubusercontent.com/AmandaRiyas/Bike-Sharing-Dataset/refs/heads/main/data/day.csv')

# Filtering data
MNDday_df['dteday'] = pd.to_datetime(MNDday_df['dteday'])
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

# Mulai Streamlit
st.title("Dashboard Analisis Penyewaan Sepeda 🚲")

# Sidebar filter
category_labels = {
    "weathersit": {1: "Cerah", 2: "Berawan", 3: "Hujan"},
    "season": {1: "Semi", 2: "Panas", 3: "Gugur", 4: "Dingin"},
    "workingday": {0: "Libur", 1: "Kerja"},
    "holiday": {0: "Biasa", 1: "Libur"},
    "weekday": {0: "Senin", 1: "Selasa", 2: "Rabu", 3: "Kamis", 4: "Jumat", 5: "Sabtu", 6: "Minggu"}
}

for col, mapping in category_labels.items():
    monthly_rentals_df[col] = monthly_rentals_df[col].replace(mapping)

selected_season = st.sidebar.selectbox("Pilih Musim:", monthly_rentals_df['season'].unique())
selected_weather = st.sidebar.selectbox("Pilih Cuaca:", monthly_rentals_df['weathersit'].unique())
selected_weekday = st.sidebar.selectbox("Pilih Hari:", monthly_rentals_df['weekday'].unique())
selected_holiday = st.sidebar.selectbox("Pilih Status Libur:", monthly_rentals_df['holiday'].unique())
selected_workingday = st.sidebar.selectbox("Pilih Status Hari Kerja:", monthly_rentals_df['workingday'].unique())

# Filter data
filtered_data = monthly_rentals_df[
    (monthly_rentals_df['season'] == selected_season) &
    (monthly_rentals_df['weathersit'] == selected_weather) &
    (monthly_rentals_df['weekday'] == selected_weekday) &
    (monthly_rentals_df['holiday'] == selected_holiday) &
    (monthly_rentals_df['workingday'] == selected_workingday)
]

# Tampilkan hasil
st.metric("Total Penyewaan", int(filtered_data['total_rentals'].sum()))
st.metric("Rata-rata Penyewaan", round(filtered_data['total_rentals'].mean(), 2))

st.dataframe(filtered_data[['month', 'season', 'weathersit', 'weekday', 'workingday', 'holiday', 'total_rentals']])

# Tambahkan visualisasi
st.bar_chart(filtered_data[['weekday', 'total_rentals']].set_index('weekday'))

# Diagram Garis per kategori
st.subheader("Tren Penyewaan Sepeda Berdasarkan Kategori")
fig, axes = plt.subplots(3, 2, figsize=(12, 12))
axes = axes.flatten()
categorical_vars = ["weathersit", "weekday", "workingday", "holiday", "season"]

for i, var in enumerate(categorical_vars):
    grouped_data = monthly_rentals_df.groupby(var)["total_rentals"].sum().reset_index()
    if var == "weekday":
        weekday_order = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
        grouped_data[var] = pd.Categorical(grouped_data[var], categories=weekday_order, ordered=True)
        grouped_data = grouped_data.sort_values(var)
    axes[i].plot(grouped_data[var], grouped_data["total_rentals"], marker='o', linestyle='-', color='b')
    axes[i].set_title(f"Total Rentals by {var.capitalize()}")
    axes[i].set_xlabel(var.capitalize())
    axes[i].set_ylabel("Total Rentals")
if len(categorical_vars) % 2 != 0:
    fig.delaxes(axes[-1])
plt.tight_layout()
st.pyplot(fig)

# Heatmap
st.subheader("Heatmap Penyewaan Berdasarkan Musim dan Cuaca")
correlation_matrix = monthly_rentals_df[['total_rentals', 'season', 'weathersit']].corr(numeric_only=True)
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", linewidths=0.5)
plt.title("Matriks Korelasi Variabel")
st.pyplot(plt)

# Barplot tambahan
plt.figure(figsize=(8, 5))
sns.barplot(data=monthly_rentals_df.reset_index(), x='season', y='total_rentals', palette='coolwarm')
plt.title("Rata-rata Penyewaan Berdasarkan Kategori Suhu")
plt.xlabel("Kategori Suhu")
plt.ylabel("Rata-rata Jumlah Penyewa")
plt.xticks(rotation=20)
plt.grid(axis="y", linestyle="--", alpha=0.7)
st.pyplot(plt)

# Kesimpulan
st.subheader("Kesimpulan")
st.markdown("""
- **Conclusion Pertanyaan 1**
  Dari seluruh proses analisis data yang telah dilakukan kita dapat disimpulkan bahwa penyewa sepeda tertinggi terjadi ketika workingday (tidak dalam masa holiday) terutama pada hari Jumat ketika cuaca cerah di musim gugur (Fall). Penyewaan sepeda terendah terjadi ketika bukan workingday (holiday) terutama hari Minggu ketika cuaca hujan/salju ringan di musim gugur (Fall).

- **Conclusion Pertanyaan 2**
  Dari seluruh proses analisis data yang telah dilakukan kita dapat disimpulkan bahwa atemp memiliki pengaruh yang kuat terhadap jumlah penyewa sepeda, semakin tinggi atemp maka semakin tinggi pula jumlah penyewa sepeda. Windspeed hanya memiliki korelasi lemah dan negatif artinya setiap windspeed meningkat akan sedikit menurunkan jumlah penyewa sepeda, dan kelembaban (hum) tidak memiliki korelasi dengan jumlah penyewa sepeda.
""")
