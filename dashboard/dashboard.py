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

df = load_data()

# Sidebar
st.sidebar.header("Dashboard Bike Sharing")
selected_viz = st.sidebar.selectbox("Pilih Visualisasi", ["Tampilkan Data", "Statistik Data", "Pengaruh Cuaca", "Pengaruh Musim"])

# Tampilkan Data
if selected_viz == "Tampilkan Data":
    st.write("## Data Penyewaan Sepeda")
    st.dataframe(df.head())

# Statistik Data
elif selected_viz == "Statistik Data":
    st.write("## Statistik Data")
    st.write(df.describe())

# Pengaruh Cuaca
elif selected_viz == "Pengaruh Cuaca":
    st.write("## Pengaruh Cuaca terhadap Penyewaan Sepeda")
    fig, ax = plt.subplots()
    sns.boxplot(x=df['weathersit'], y=df['cnt'], ax=ax)
    ax.set_xlabel("Cuaca")
    ax.set_ylabel("Jumlah Penyewaan")
    st.pyplot(fig)

# Pengaruh Musim
elif selected_viz == "Pengaruh Musim":
    st.write("## Pengaruh Musim terhadap Penyewaan Sepeda")
    fig, ax = plt.subplots()
    sns.boxplot(x=df['season'], y=df['cnt'], ax=ax)
    ax.set_xlabel("Musim")
    ax.set_ylabel("Jumlah Penyewaan")
    st.pyplot(fig)

