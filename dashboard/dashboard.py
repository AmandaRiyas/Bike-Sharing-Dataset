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
selected_viz = st.sidebar.selectbox("Pilih Visualisasi", ["Tampilkan Data", "Statistik Data", "Pengaruh Cuaca", "Pengaruh Musim", "Kesimpulan"])

# Tampilkan Data
if selected_viz == "Tampilkan Data":
    st.write("## Data Penyewaan Sepeda")
    st.dataframe(data.head())

# Statistik Data
elif selected_viz == "Statistik Data":
    st.write("## Statistik Data")
    st.write(data.describe())

# Pengaruh Cuaca
elif selected_viz == "Pengaruh Cuaca":
    st.write("## Pengaruh Cuaca terhadap Penyewaan Sepeda")
    
    # Diagram Garis Cuaca
    garis_cuaca = data.groupby('weathersit')['cnt'].mean().reset_index()
    fig, ax = plt.subplots(figsize=(8,5))
    sns.lineplot(x=garis_cuaca["weathersit"], y=garis_cuaca["cnt"], marker="o", linewidth=2)
    ax.set_title("Hubungan Cuaca dengan Penyewa Sepeda")
    ax.set_xlabel("Weathersit")
    ax.set_ylabel("Jumlah Penyewa")
    st.pyplot(fig)
    
    # Boxplot Cuaca
    fig, ax = plt.subplots()
    sns.boxplot(x=data['weathersit'], y=data['cnt'], ax=ax)
    ax.set_xlabel("Cuaca")
    ax.set_ylabel("Jumlah Penyewaan")
    st.pyplot(fig)
    
    st.write("**Analisis:** Dari diagram garis terlihat bahwa semakin besar kategori garis menurun, artinya pada cuaca dengan kategori 1(clear, few clouds, partly cloudy) banyak yang menyewa sepeda, namun pada cuaca kategori ke 2 (Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist) mulai menurun, dan yang paling rendah pada cuaca pada kategori 3 (Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds). Kemudian pada boxplot dapat diketahui informasi distribusi data cuaca kategori 1 luas terbukti dari rentangnya yang cukup panjang, untuk kategori cuaca kategori 2 juga luas tapi masih di bawah kategori 1, dan distribusi cuaca kategori 3 paling rendah diantara kategori lain terbukti dari rentang yang lebih pendek dari kategori 1 maupun 2.")

# Pengaruh Musim
elif selected_viz == "Pengaruh Musim":
    st.write("## Pengaruh Musim terhadap Penyewaan Sepeda")
    
    # Diagram Garis Musim
    garis_musim = data.groupby('season')['cnt'].mean().reset_index()
    fig, ax = plt.subplots(figsize=(8,5))
    sns.lineplot(x=garis_musim["season"], y=garis_musim["cnt"], marker="o", linewidth=2)
    ax.set_title("Pengaruh Perbedaan Musim dengan Penyewaan Sepeda")
    ax.set_xlabel("Season")
    ax.set_ylabel("Jumlah Penyewa")
    st.pyplot(fig)
    
    # Boxplot Musim
    fig, ax = plt.subplots()
    sns.boxplot(x=data['season'], y=data['cnt'], ax=ax)
    ax.set_xlabel("Musim")
    ax.set_ylabel("Jumlah Penyewaan")
    st.pyplot(fig)
    
    st.write("**Analisis:** Dari diagram garis terlihat bahwa pada season 1 (spring) ke season 2 (summer) ke season 3 (fall) terus mengalami peningkatan, namun pada season 4 (winter) mengalami penurunan penyewaan sepeda. Kemudian pada boxplot dapat diketahui informasi distribusi data musim, distribusi terluas adalah musim kategori 4, disusul kategori 2 dan 3 yang luasnya hampir mirip dan yang paling sempit adalah distribusi musim kategori 1, pada boxplot tersebut hanya ada sedikit outlier sehingga penyewaan sudah termasuk konsisten.")

# Kesimpulan
elif selected_viz == "Kesimpulan":
    st.write("## Kesimpulan")
    st.write(
        "**Kesimpulan:**\n"
        " Cuaca dan musim memiliki pengaruh terhadap banyaknya penyewa sepeda, namun masih ada kemungkinan variabel lain yang memengaruhi banyaknya penyewa sepeda\n"
    )
