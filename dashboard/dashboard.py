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

# Mapping kategori
category_labels = {
    "weathersit": {1: "Cerah", 2: "Berawan", 3: "Hujan/Salju Ringan"},
    "weekday": {0: "Minggu", 1: "Senin", 2: "Selasa", 3: "Rabu", 4: "Kamis", 5: "Jumat", 6: "Sabtu"},
    "workingday": {0: "Tidak", 1: "Ya"},
    "holiday": {0: "Tidak", 1: "Ya"},
    "season": {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
}

# Mulai Streamlit
st.title("Dashboard Analisis Penyewaan Sepeda")

# Sidebar filter
selected_month = st.sidebar.selectbox("Pilih Bulan:", MNDday_df['month'].unique())

# Filter data
filtered_data = monthly_rentals_df[
    (MNDday_df['month'] == selected_month)
]

st.dataframe(filtered_data[['month', 'season', 'weathersit', 'weekday', 'workingday', 'holiday', 'total_rentals']])

# Visualisasi kategori
fig, axes = plt.subplots(3, 2, figsize=(12, 12))
axes = axes.flatten()
categorical_vars = ["weathersit", "weekday", "workingday", "holiday", "season"]
for i, var in enumerate(categorical_vars):
    grouped_data = monthly_rentals_df.groupby(var)["total_rentals"].sum().reset_index()
    if var in category_labels:
        grouped_data[var] = grouped_data[var].replace(category_labels[var])
    axes[i].plot(grouped_data[var], grouped_data["total_rentals"], marker='o', linestyle='-', color='b')
    axes[i].set_title(f"Total Rentals by {var.capitalize()}")
    axes[i].set_xlabel(var.capitalize())
    axes[i].set_ylabel("Total Rentals")
if len(categorical_vars) % 2 != 0:
    fig.delaxes(axes[-1])
plt.tight_layout()
st.pyplot(fig)

# Heatmap Korelasi
st.subheader("Heatmap Korelasi Variabel")
plt.figure(figsize=(8, 6))
correlation_matrix = MNDday_df[['atemp', 'hum', 'windspeed', 'cnt']].corr()
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", linewidths=0.5)
st.pyplot(plt)

# Rata-rata Penyewaan Berdasarkan Suhu
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

# Kesimpulan
st.subheader("Kesimpulan")
st.markdown("""
- **Conclusion Pertanyaan 1**
  Penyewa sepeda tertinggi terjadi saat hari kerja, Jumat, cuaca cerah di musim gugur. Penyewaan terendah terjadi saat libur, Minggu, hujan ringan di musim gugur.

- **Conclusion Pertanyaan 2**
  Atemp punya pengaruh kuat terhadap penyewa sepeda. Windspeed lemah dan negatif, hum hampir tidak ada korelasi.
""")
