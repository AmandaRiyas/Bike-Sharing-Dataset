import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter

# Load data
@st.cache_data
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

plt.style.use('default')  # Ensure consistent style

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
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(daily_orders_df["Date"], daily_orders_df["Jumlah Penyewa"], marker='o', linewidth=2, color="#72BCD4")
ax.set_title("Penyewa Sepeda", loc="center", fontsize=20)
ax.tick_params(axis='x', rotation=45, labelsize=10)
ax.tick_params(axis='y', labelsize=10)
plt.tight_layout()
st.pyplot(fig)

# Mappings
weather_mapping = {1: 'Cerah', 2: 'Berawan', 3: 'Hujan/Salju ringan'}
weekday_mapping = {0: 'Minggu', 1: 'Senin', 2: 'Selasa', 3: 'Rabu', 4: 'Kamis', 5: 'Jumat', 6: 'Sabtu'}
workingday_mapping = {0: 'Tidak', 1: 'Ya'}
holiday_mapping = {0: 'Tidak', 1: 'Ya'}
season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}

# Weather vs Count
data['cuaca'] = data['weathersit'].map(weather_mapping)
summary_cuaca = data.groupby('cuaca')['cnt'].agg(["sum"])

fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(summary_cuaca.index, summary_cuaca['sum'], color=["#72BCD4", "#B0BEC5", "#90A4AE"])
ax.set_title("Jumlah Penyewa Berdasarkan Cuaca", fontsize=15)
ax.yaxis.set_major_formatter(FuncFormatter(juta))
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(fig)

# Weekday vs Count
data['weekday_label'] = data['weekday'].map(weekday_mapping)
summary_weekday = data.groupby('weekday_label')['cnt'].agg(["sum"])

fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(summary_weekday.index, summary_weekday['sum'], color=["#72BCD4", "#B0BEC5", "#90A4AE"])
ax.set_title("Jumlah Penyewa Berdasarkan Weekday", fontsize=15)
ax.yaxis.set_major_formatter(FuncFormatter(juta))
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(fig)

# Workingday vs Count
data['workingday_label'] = data['workingday'].map(workingday_mapping)
summary_workingday = data.groupby('workingday_label')['cnt'].agg(["sum"])

fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(summary_workingday.index, summary_workingday['sum'], color=["#72BCD4", "#B0BEC5", "#90A4AE"])
ax.set_title("Jumlah Penyewa Berdasarkan Workingday", fontsize=15)
ax.yaxis.set_major_formatter(FuncFormatter(format_ribu))
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(fig)

# Holiday vs Count
data['holiday_label'] = data['holiday'].map(holiday_mapping)
summary_holiday = data.groupby('holiday_label')['cnt'].agg(["sum"])

fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(summary_holiday.index, summary_holiday['sum'], color=["#72BCD4", "#B0BEC5", "#90A4AE"])
ax.set_title("Jumlah Penyewa Berdasarkan Holiday", fontsize=15)
ax.yaxis.set_major_formatter(FuncFormatter(format_ribu))
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(fig)

# Season vs Count
data['season_label'] = data['season'].map(season_mapping)
summary_season = data.groupby('season_label')['cnt'].agg(["sum"])

fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(summary_season.index, summary_season['sum'], color=["#72BCD4", "#B0BEC5", "#90A4AE"])
ax.set_title("Jumlah Penyewa Berdasarkan Musim", fontsize=15)
ax.yaxis.set_major_formatter(FuncFormatter(juta))
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(fig)

# Heatmap Correlation
correlation_matrix = data[['cnt', 'atemp', 'hum', 'windspeed']].corr()
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", linewidths=0.5)
ax.set_title("Matriks Korelasi Variabel")
st.pyplot(fig)

# Conclusion
st.subheader('Kesimpulan')
st.write("- Dari seluruh proses analisis data yang telah dilakukan dapat disimpulkan pola penyewaan sepeda berdasarkan kondisi cuaca, weekday, workingday, holiday, dan season.")
