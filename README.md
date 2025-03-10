# Analisis Data Bike Sharing Dataset

## Deskripsi Proyek
Proyek ini menganalisis dataset penyewaan sepeda menggunakan **Bike Sharing Dataset**. Analisis mencakup pengaruh cuaca dan musim terhadap jumlah penyewaan sepeda.

## Dataset
Dataset yang digunakan diambil dari:
[https://raw.githubusercontent.com/AmandaRiyas/Bike-Sharing-Dataset/refs/heads/main/day.csv](https://raw.githubusercontent.com/AmandaRiyas/Bike-Sharing-Dataset/refs/heads/main/day.csv)

### **Fitur-Fitur Utama dalam Dataset:**
- `season` : Musim (1: Winter, 2: Spring, 3: Summer, 4: Fall)
- `weathersit` : Kondisi cuaca (1: Cerah, 2: Berawan, 3: Hujan, 4: Badai)
- `cnt` : Total jumlah penyewaan sepeda
- `temp`, `hum`, `windspeed` : Variabel cuaca lainnya

##  Cara Menjalankan Dashboard
Proyek ini menggunakan **Streamlit** untuk membuat dashboard interaktif.

### **1. Instalasi Dependensi**
Pastikan Anda telah menginstal pustaka yang diperlukan:
```bash
pip install pandas numpy matplotlib seaborn streamlit
```

### **2. Jalankan Dashboard**
Gunakan perintah berikut untuk menjalankan Streamlit:
```bash
streamlit run dashboard.py
```

## Fitur Dashboard
- **Tampilkan Data** → Menampilkan beberapa data awal dari dataset.
- **Statistik Data** → Menampilkan ringkasan statistik deskriptif.
- **Pengaruh Cuaca** → Visualisasi hubungan antara kondisi cuaca dan jumlah penyewaan sepeda.
- **Pengaruh Musim** → Visualisasi hubungan antara musim dan jumlah penyewaan sepeda.

## Teknologi yang Digunakan
- **Python**
- **Pandas & NumPy**
- **Matplotlib & Seaborn**
- **Streamlit**

---

