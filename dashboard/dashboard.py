import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load dataset
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/AmandaRiyas/Bike-Sharing-Dataset/refs/heads/main/day.csv"
    df = pd.read_csv(url)
    return df

data = load_data()

# Set title
st.title('Bike Sharing Dashboard')

# Sidebar
st.sidebar.header("Dashboard Bike Sharing")
selected_viz = st.sidebar.selectbox("Pilih Visualisasi", ["Tampilkan Data", "Statistik Data", "Pengaruh Cuaca & Musim"])

# Tampilkan Data
if selected_viz == "Tampilkan Data":
    st.write("## Data Penyewaan Sepeda")
    st.dataframe(data.head())

# Statistik Data
elif selected_viz == "Statistik Data":
    st.write("## Statistik Data")
    st.write(data.describe())

# Pengaruh Cuaca & Musim
elif selected_viz == "Pengaruh Cuaca & Musim":
    st.write("## Pengaruh Cuaca dan Musim terhadap Penyewaan Sepeda")
    
    # Boxplot Cuaca
    st.write("### Pengaruh Cuaca")
    fig, ax = plt.subplots()
    sns.boxplot(x=data['weathersit'], y=data['cnt'], ax=ax)
    ax.set_xlabel("Cuaca")
    ax.set_ylabel("Jumlah Penyewaan")
    st.pyplot(fig)
    
    # Boxplot Musim
    st.write("### Pengaruh Musim")
    fig, ax = plt.subplots()
    sns.boxplot(x=data['season'], y=data['cnt'], ax=ax)
    ax.set_xlabel("Musim")
    ax.set_ylabel("Jumlah Penyewaan")
    st.pyplot(fig)
    
    # Analisis
    st.write("📌 **Kesimpulan:** Dari diagram garis terlihat bahwa semakin besar kategori garis menurun, artinya pada cuaca dengan kategori 1(clear, few clouds, partly cloudy) banyak yang menyewa sepeda, namun pada cuaca kategori ke 2 (Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist) mulai menurun, dan yang paling rendah pada cuaca pada kategori 3 (Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds). Kemudian pada boxplot dapat diketahui informasi distribusi data cuaca kategori 1 luas terbukti dari rentangnya yang cukup panjang, untuk kategori cuaca kategori 2 juga luas tapi masih di bawah kategori 1, dan distribusi cuaca kategori 3 paling rendah diantara kategori lain terbukti dari rentang yang lebih pendek dari kategori 1 maupun 2.")
    
    # Tren Penyewaan Berdasarkan Cuaca
    st.write("### Tren Penyewaan Sepeda Berdasarkan Cuaca")
    fig, ax = plt.subplots()
    sns.lineplot(x=data['dteday'], y=data['cnt'], hue=data['weathersit'], ax=ax)
    ax.set_xlabel('Tanggal')
    ax.set_ylabel('Jumlah Penyewaan Harian')
    plt.xticks(rotation=45)
    st.pyplot(fig)
    
    # Tren Penyewaan Berdasarkan Musim
    st.write("### Tren Penyewaan Sepeda Berdasarkan Musim")
    fig, ax = plt.subplots()
    sns.lineplot(x=data['dteday'], y=data['cnt'], hue=data['season'], ax=ax)
    ax.set_xlabel('Tanggal')
    ax.set_ylabel('Jumlah Penyewaan Harian')
    plt.xticks(rotation=45)
    st.pyplot(fig)
    
    # Analsiis
    st.write("📌 **Analisis:** Dari diagram garis terlihat bahwa pada season 1 (spring) ke season 2 (summer) ke season 3 (fall) terus mengalami peningkatan, namun pada season 4 (winter) mengalami penurunan penyewaan sepeda. Kemudian pada boxplot dapat diketahui informasi distribusi data musim, distribusi terluas adalah musim kategori 4, disusul kategori 2 dan 3 yang luasnya hampir mirip dan yang paling sempit adalah distribusi musim kategori 1, pada boxplot tersebut hanya ada sedikit outlier sehingga penyewaan sudah termasuk konsisten.")

# Kesimpulan
st.write("## Kesimpulan")
st.write(
    " Musim dan cuaca memiliki pengaruh pada jumlah penyewaan sepeda meskipun masih ada kemungkinan variabel lain yang mempengaruhi peningkatan penyewaan sepeda."
)
