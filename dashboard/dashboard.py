import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter

# Load data
@st.cache
def load_data():
    data = pd.read_csv('https://raw.githubusercontent.com/AmandaRiyas/Bike-Sharing-Dataset/refs/heads/main/data/day.csv')
    data['dteday'] = pd.to_datetime(data['dteday'])
    return data

data = load_data()

# Define daily order function
def daily_order_df(df):
    daily_orders_df = df.resample(rule='D', on='dteday').agg({
        "cnt": "sum"
    })
    daily_orders_df = daily_orders_df.reset_index()
    daily_orders_df.rename(columns={
        "dteday": "Date",
        "cnt": "Jumlah Penyewa"
    }, inplace=True)
    
    return daily_orders_df

# Formatter for large numbers
def format_ribu(x, _):
    return f'{int(x/1e3)} Ribu' if x >= 1e3 else f'{int(x)}'

def juta(x, _):
    return f'{int(x/1e6)} Juta' if x >= 1e6 else f'{int(x/1e3)} Ribu'

# Sidebar for date filtering
st.sidebar.header('Filter Data')
start_date = st.sidebar.date_input('Start date', data['dteday'].min().date())
end_date = st.sidebar.date_input('End date', data['dteday'].max().date())

filtered_data = data[(data['dteday'].dt.date >= start_date) & (data['dteday'].dt.date <= end_date)]

# Dashboard title
st.title('Bike Rentals Dashboard')
st.write(f"Showing data from {start_date} to {end_date}")

# Daily Order Chart
daily_orders_df = daily_order_df(filtered_data)
plt.figure(figsize=(10, 5))
plt.plot(daily_orders_df["Date"], daily_orders_df["Jumlah Penyewa"], marker='o', linewidth=2, color="#72BCD4")
plt.title("Penyewa Sepeda", loc="center", fontsize=20)
plt.xticks(rotation=45, ha="right", fontsize=10)
plt.yticks(fontsize=10)
plt.tight_layout()
st.pyplot(plt)
plt.close()

# Conclusion
st.subheader('Kesimpulan')
st.write("- Dari seluruh proses analisis data yang telah dilakukan dapat disimpulkan pola penyewaan sepeda berdasarkan kondisi cuaca, weekday, workingday, holiday, dan season yaitu penyewa sepeda tertinggi terjadi ketika workingday (tidak dalam masa holiday) terutama pada hari Jumat ketika cuaca cerah di musim gugur (Fall). Penyewaan sepeda terendah terjadi ketika bukan workingday (holiday) terutama hari Minggu ketika cuaca hujan/salju ringan di musim gugur (Fall).")
st.write("- Dari seluruh proses analisis data yang telah dilakukan dapat disimpulkan pengaruh dari atempt, hum, windspeed terhadap banyaknya penyewa sepeda yaitu atemp memiliki pengaruh yang kuat terhadap jumlah penyewa sepeda, semakin tinggi atemp maka semakin tinggi pula jumlah penyewa sepeda. Windspeed hanya memiliki korelasi lemah dan negatif, artinya setiap windspeed meningkat akan sedikit menurunkan jumlah penyewa sepeda, dan kelembaban (hum) tidak memiliki korelasi dengan jumlah penyewa sepeda.")
