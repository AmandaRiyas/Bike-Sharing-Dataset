import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from tabulate import tabulate

# Load data dari file terbaru
MNDday_df = pd.read_csv('https://raw.githubusercontent.com/AmandaRiyas/Bike-Sharing-Dataset/refs/heads/main/data/day.csv')

# Filtering data sesuai kode
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

# Dashboard Streamlit
st.title("Dashboard Analisis Penyewaan Sepeda 🚲")

# Sidebar filter lebih lengkap
selected_season = st.sidebar.selectbox("Pilih Musim:", monthly_rentals_df['season'].unique())
selected_weather = st.sidebar.selectbox("Pilih Cuaca:", monthly_rentals_df['weathersit'].unique())
selected_weekday = st.sidebar.selectbox("Pilih Hari:", monthly_rentals_df['weekday'].unique())

# Filter data
filtered_data = monthly_rentals_df[
    (monthly_rentals_df['season'] == selected_season) &
    (monthly_rentals_df['weathersit'] == selected_weather) &
    (monthly_rentals_df['weekday'] == selected_weekday)
]

# Tampilkan hasil
st.metric("Total Penyewaan", int(filtered_data['total_rentals'].sum()))
st.metric("Rata-rata Penyewaan", round(filtered_data['total_rentals'].mean(), 2))

st.dataframe(filtered_data[['month', 'season', 'weathersit', 'weekday', 'workingday', 'holiday', 'total_rentals']])

# Diagram Garis per kategori
st.subheader("Tren Penyewaan Sepeda Berdasarkan Kategori")
categorical_vars = ["weathersit", "weekday", "workingday", "holiday", "season"]
category_labels = {
    "weathersit": {1: "Cerah", 2: "Berawan", 3: "Hujan"},
    "season": {1: "Semi", 2: "Panas", 3: "Gugur", 4: "Dingin"},
    "workingday": {0: "Libur", 1: "Kerja"},
    "holiday": {0: "Biasa", 1: "Libur"},
    "weekday": {0: "Senin", 1: "Selasa", 2: "Rabu", 3: "Kamis", 4: "Jumat", 5: "Sabtu", 6: "Minggu"}
}

for var in categorical_vars:
    grouped_data = monthly_rentals_df.groupby(var)["total_rentals"].sum().reset_index()
    if var in category_labels:
        grouped_data[var] = grouped_data[var].replace(category_labels[var])

    fig, ax = plt.subplots()
    ax.plot(grouped_data[var], grouped_data["total_rentals"], marker='o', linestyle='-', color='b')
    ax.set_title(f"Total Rentals by {var.capitalize()}")
    ax.set_xlabel(var.capitalize())
    ax.set_ylabel("Total Rentals")
    st.pyplot(fig)

# Heatmap
st.subheader("Heatmap Penyewaan Berdasarkan Musim dan Cuaca")
correlation_matrix = monthly_rentals_df[['total_rentals', 'season', 'weathersit', 'weekday', 'workingday', 'holiday']].corr()
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", linewidths=0.5)
plt.title("Matriks Korelasi Variabel")
st.pyplot(plt)

# Analisis Clustering
MNDday_df['season'] = MNDday_df['season'].astype(str)
MNDday_df['weathersit'] = MNDday_df['weathersit'].astype(str)
MNDday_df['weekday'] = MNDday_df['weekday'].astype(str)
MNDday_df['workingday'] = MNDday_df['workingday'].astype(str)
MNDday_df['holiday'] = MNDday_df['holiday'].astype(str)
MNDday_df['cluster_manual'] = (
    MNDday_df['season'] + "_" +
    MNDday_df['weathersit'] + "_" +
    MNDday_df['weekday'] + "_" +
    MNDday_df['workingday'] + "_" +
    MNDday_df['holiday']
)
custom_cluster_summary = MNDday_df.groupby('cluster_manual').agg(
    mean=('cnt', 'mean'),
    sum=('cnt', 'sum'),
    count=('cnt', 'count')
).reset_index()

st.subheader("Clustering Manual")
st.dataframe(custom_cluster_summary)

# Kesimpulan
st.subheader("Kesimpulan")
st.write("- **Kesimpulan Pertanyaan 1:** Penyewa sepeda tertinggi terjadi saat workingday, hari Jumat, cuaca cerah di musim gugur.")
st.write("- **Kesimpulan Pertanyaan 2:** Atemp berpengaruh kuat, windspeed negatif lemah, hum tidak berpengaruh pada jumlah penyewa.")
