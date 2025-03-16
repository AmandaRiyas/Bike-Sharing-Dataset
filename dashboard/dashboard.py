import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Load data dari link
MNDday_df = pd.read_csv('https://raw.githubusercontent.com/AmandaRiyas/Bike-Sharing-Dataset/refs/heads/main/data/day.csv')

# Filtering data
MNDday_df['dteday'] = pd.to_datetime(MNDday_df['dteday'])
MNDday_df['month'] = MNDday_df['dteday'].dt.strftime('%B')
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
st.title("Dashboard Analisis Penyewaan Sepeda")

# Sidebar filter
selected_month = st.sidebar.selectbox("Pilih Bulan:", MNDday_df['month'].unique())

# Filter data
filtered_data = monthly_rentals_df[
    (MNDday_df['month'] == selected_month)
]

st.dataframe(filtered_data[['month', 'season', 'weathersit', 'weekday', 'workingday', 'holiday', 'total_rentals']])

# Heatmap Korelasi
st.subheader("Heatmap Korelasi Variabel")
plt.figure(figsize=(8, 6))
correlation_matrix = MNDday_df[['atemp', 'hum', 'windspeed', 'cnt']].corr()
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", linewidths=0.5)
st.pyplot(plt)

# Diagram Batang Rata-rata Penyewaan Berdasarkan Suhu
st.subheader("Rata-rata Penyewaan Berdasarkan Kategori Suhu")
MNDday_df['atemp_label'] = pd.cut(MNDday_df['atemp'], bins=[0, 0.3, 0.6, 1.0], labels=['Dingin', 'Sedang', 'Panas'])
summary_atemp = MNDday_df.groupby('atemp_label')['cnt'].agg(['mean']).reset_index()
plt.figure(figsize=(8, 5))
sns.barplot(data=summary_atemp, x='atemp_label', y='mean', palette='coolwarm')
plt.title("Rata-rata Penyewaan Berdasarkan Kategori Suhu")
plt.xlabel("Kategori Suhu")
plt.ylabel("Rata-rata Jumlah Penyewa")
plt.xticks(rotation=20)
plt.grid(axis="y", linestyle="--", alpha=0.7)
st.pyplot(plt)

# Visualisasi Weathersit
st.subheader("Distribusi Penyewaan Berdasarkan Cuaca")
plt.figure(figsize=(8, 5))
sns.countplot(data=MNDday_df, x='weathersit', palette='pastel')
plt.title("Distribusi Cuaca")
plt.xlabel("Cuaca")
plt.ylabel("Jumlah Hari")
st.pyplot(plt)

# Visualisasi Season
st.subheader("Distribusi Penyewaan Berdasarkan Musim")
plt.figure(figsize=(8, 5))
sns.countplot(data=MNDday_df, x='season', palette='viridis')
plt.title("Distribusi Musim")
plt.xlabel("Musim")
plt.ylabel("Jumlah Hari")
st.pyplot(plt)

# Visualisasi Weekday
st.subheader("Distribusi Penyewaan Berdasarkan Hari")
plt.figure(figsize=(8, 5))
sns.countplot(data=MNDday_df, x='weekday', palette='muted')
plt.title("Distribusi Hari")
plt.xlabel("Hari")
plt.ylabel("Jumlah Hari")
st.pyplot(plt)

# Visualisasi Holiday
st.subheader("Distribusi Penyewaan Berdasarkan Status Libur")
plt.figure(figsize=(8, 5))
sns.countplot(data=MNDday_df, x='holiday', palette='coolwarm')
plt.title("Distribusi Status Libur")
plt.xlabel("Libur")
plt.ylabel("Jumlah Hari")
st.pyplot(plt)

# Visualisasi Workingday
st.subheader("Distribusi Penyewaan Berdasarkan Status Hari Kerja")
plt.figure(figsize=(8, 5))
sns.countplot(data=MNDday_df, x='workingday', palette='Set2')
plt.title("Distribusi Hari Kerja")
plt.xlabel("Hari Kerja")
plt.ylabel("Jumlah Hari")
st.pyplot(plt)

# Kesimpulan
st.subheader("Kesimpulan")
st.markdown("""
- **Conclusion Pertanyaan 1**
  Penyewa sepeda tertinggi terjadi saat hari kerja, Jumat, cuaca cerah di musim gugur. Penyewaan terendah terjadi saat libur, Minggu, hujan ringan di musim gugur.

- **Conclusion Pertanyaan 2**
  Atemp punya pengaruh kuat terhadap penyewa sepeda. Windspeed lemah dan negatif, hum hampir tidak ada korelasi.
""")
