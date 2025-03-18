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

# Common style for all bar charts
def create_bar_chart(data, title, color_list):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(data.index, data['sum'], color=color_list)
    ax.set_title(title, fontsize=15)
    ax.yaxis.set_major_formatter(FuncFormatter(format_ribu))
    plt.xticks(rotation=0)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig)

# Ensure consistent category order
weather_order = ['Cerah', 'Berawan', 'Hujan/Salju ringan']
weekday_order = ['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu']
workingday_order = ['Tidak', 'Ya']
holiday_order = ['Tidak', 'Ya']
season_order = ['Spring', 'Summer', 'Fall', 'Winter']

# Weather vs Count
data['cuaca'] = data['weathersit'].map(weather_mapping)
summary_cuaca = data.groupby('cuaca')['cnt'].agg(["sum"]).reindex(weather_order)
create_bar_chart(summary_cuaca, "Jumlah Penyewa Berdasarkan Cuaca", ["#72BCD4", "#B0BEC5", "#90A4AE"])

# Weekday vs Count
data['weekday_label'] = data['weekday'].map(weekday_mapping)
summary_weekday = data.groupby('weekday_label')['cnt'].agg(["sum"]).reindex(weekday_order)
create_bar_chart(summary_weekday, "Jumlah Penyewa Berdasarkan Weekday", ["#72BCD4", "#B0BEC5", "#90A4AE"])

# Workingday vs Count
data['workingday_label'] = data['workingday'].map(workingday_mapping)
summary_workingday = data.groupby('workingday_label')['cnt'].agg(["sum"]).reindex(workingday_order)
create_bar_chart(summary_workingday, "Jumlah Penyewa Berdasarkan Workingday", ["#72BCD4", "#B0BEC5","#90A4AE"])

# Holiday vs Count
data['holiday_label'] = data['holiday'].map(holiday_mapping)
summary_holiday = data.groupby('holiday_label')['cnt'].agg(["sum"]).reindex(holiday_order)
create_bar_chart(summary_holiday, "Jumlah Penyewa Berdasarkan Holiday", ["#72BCD4", "#B0BEC5","#90A4AE"])

# Season vs Count
data['season_label'] = data['season'].map(season_mapping)
summary_season = data.groupby('season_label')['cnt'].agg(["sum"]).reindex(season_order)
create_bar_chart(summary_season, "Jumlah Penyewa Berdasarkan Musim", ["#72BCD4", "#B0BEC5", "#90A4AE"])

# Heatmap Correlation
hubungan = data[['atemp', 'hum', 'windspeed', 'cnt']]
correlation_matrix = hubungan.corr()
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", linewidths=0.5)
plt.title("Korelasi")
st.pyplot(plt.gcf())

# Suhu terasa analysis
MNDday_df = data.copy()
MNDday_df['atemp_actual'] = MNDday_df['atemp'] * 50
average_atemp = MNDday_df['atemp_actual'].mean()
tolerance = 2

# Correcting labels

def label_temp(row):
    if row['atemp_actual'] < (average_atemp - tolerance):
        return 'Normal'
    elif (average_atemp - tolerance) <= row['atemp_actual'] <= (average_atemp + tolerance):
        return 'Di Bawah Rata-rata'
    else:
        return 'Di Atas Rata-rata'

MNDday_df['atemp_label'] = MNDday_df.apply(label_temp, axis=1)
summary_atemp = MNDday_df.groupby('atemp_label')['cnt'].agg(["mean"]).sort_values('mean', ascending=False)

plt.figure(figsize=(8, 5))
sns.barplot(data=summary_atemp.reset_index(), x='atemp_label', y='mean', palette='coolwarm')
plt.title("Rata-rata Penyewaan Berdasarkan Kategori Suhu")
plt.xlabel("Kategori Suhu")
plt.ylabel("Rata-rata Jumlah Penyewa")
st.pyplot(plt.gcf())

# Conclusion
st.subheader('Kesimpulan')
st.write("- Dari seluruh proses analisis data yang telah dilakukan dapat disimpulkan pola penyewaan sepeda berdasarkan kondisi cuaca, weekday, workingday, holiday, dan season yaitu penyewa sepeda tertinggi terjadi ketika workingday (tidak dalam masa holiday) terutama pada hari Jumat ketika cuaca cerah di musim gugur(Fall). Penyewaan sepeda terendah terjadi ketika bukan workingday (holiday) terutama hari Minggu ketika cuaca hujan/salju ringan di musim gugur (Fall) ")
st.write("- Dari seluruh proses analisis data yang telah dilakukan dapat disimpulkan pengaruh dari atempt, hum, windspeed terhadap banyaknya penyewa sepeda yaitu atemp memiliki pengaruh yang kuat terhadap jumlah penyewa sepeda, semakin tinggi atempt maka semakin tinggi pula jumlah penyewa sepeda, windspeed hanya memiliki korelasi lemah dan negatif artinya setiap windspeed meningkat akan sedikit menurunkan jumlah penyewa sepeda, dan kelembaban (hum) tidak memiliki korelasi dengan jumlah penyewa sepeda.")
