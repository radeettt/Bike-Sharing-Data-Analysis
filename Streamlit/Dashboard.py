import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

st.set_option('deprecation.showPyplotGlobalUse', False)


data = pd.read_csv("https://raw.githubusercontent.com/radeettt/Bike-Sharing-Data-Analysis/main/dataset.csv")

datetime_columns = ["Date"]
data.sort_values(by="Date", inplace=True)
data.reset_index(inplace=True)

for column in datetime_columns:
    data[column] = pd.to_datetime(data[column])

min_date = data["Date"].min()
max_date = data["Date"].max()

with st.sidebar:
    st.image("https://raw.githubusercontent.com/radeettt/Bike-Sharing-Data-Analysis/main/bikes.jpg")
    
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = data[(data["Date"] >= str(start_date)) & 
                (data["Date"] <= str(end_date))]

st.header('Bike Sharing :sparkles:')
st.subheader('Bike Rental')

col1, col2 = st.columns(2)

with col1:
    total_transaction = data['Total'].count()
    st.metric("Total Transaction", value=total_transaction)

with col2:
    total_rent = data['Total'].sum() 
    st.metric("Total Rent Bikes", value=total_rent)

batas = [0, 18, 37, 57]
labels = ['safe', 'normal', 'dangerous']
data['safety'] = pd.cut(data['windspeed'], bins=batas, labels=labels, include_lowest=True)

# Membuat fungsi untuk mengelompokkan jam menjadi day atau night
def categorize_daynight(Hour):
    if 6 <= Hour <= 17:
        return 'day'
    else:
        return 'night'

data['daynight'] = data['Hour'].apply(categorize_daynight)

#PERTANYAAN 1
st.subheader('Pada musim apa pengguna dari bike rental memiliki jumlah tertinggi dan apa yang memengaruhinya?')

# Menghitung rata-rata jumlah pengguna pada setiap musim
average_per_season = data.groupby('Season')['Total'].mean().reset_index()

# Membuat dua subplot, satu untuk bar plot dan satu untuk count plot
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(15, 6))

# Bar plot untuk rata-rata jumlah pengguna pada setiap musim
sns.barplot(x='Season', y='Total', data=average_per_season, palette='pastel', ax=axes[0])
axes[0].set_title('Rata-Rata Jumlah Pengguna Berdasarkan Musim')
axes[0].set_xlabel('Musim')
axes[0].set_ylabel('Rata-rata Jumlah Pengguna')

# Count plot untuk tingkat safety berdasarkan musim
sns.countplot(x='Season', hue='safety', data=data, palette='pastel', ax=axes[1])
axes[1].set_title('Tingkat Safety Berdasarkan Musim')
axes[1].set_xlabel('Musim')
axes[1].set_ylabel('Jumlah pada Tingkat Safety')
axes[1].legend(title='Safety', loc='upper right')

# Menampilkan subplot
plt.tight_layout()
st.pyplot()

# Hitung tingkat keamanan pada tiap musim
safety_counts = data.groupby(['Season', 'safety']).size().unstack(fill_value=0)

# Hitung total observasi pada tiap musim
total_counts = data.groupby('Season').size()

# Hitung tingkat keamanan sebagai proporsi dari total observasi
safety_rate = safety_counts.div(total_counts, axis=0)
st.title('Safety Rate')
st.dataframe(safety_rate)

# Simpan teks dalam variabel
line1 = "Jumlah tertinggi pengguna dari bike rental terdapat pada musim gugur."
line2 = "Hal ini dipengaruhi oleh tingkat safety pada musim gugur yang merupakan tertinggi dibandingkan dengan musim yang lainnya."
line3 = "Tingkat safety pada musim gugur yaitu mencapai 0,82."
line4 = "Tingkat safety ini menunjukkan keamanan yang lebih tinggi, sehingga banyak pengguna memilih untuk menggunakan layanan rental sepeda pada musim gugur."

# Tampilkan teks dalam tiga baris
st.text(line1)
st.text(line2)
st.text(line3)
st.text(line4)

#PERTANYAAN 2
st.subheader('Waktu mana (Day atau Night) yang memiliki dampak pengguna terbesar untuk bike rental?')
# Hitung total pengguna pada siang dan malam
total_users_by_daynight = data.groupby('daynight')['Total'].sum()

# Buat Visualisasi Data
plt.figure(figsize=(8, 8))
plt.pie(total_users_by_daynight, labels=total_users_by_daynight.index, autopct='%1.1f%%', colors=['blue', 'red'])
plt.title('Dampak Pengguna Bike Rental pada Siang dan Malam')
st.pyplot()

line1 = "Waktu yang memiliki dampak pengguna terbesar untuk bike rental adalah day  yaitu mencapai 66.8%."
line2 = "Hal ini karena jumlah pengguna bike rental saat day dua kali lipat lebih tinggi dibandingkan dengan night."
st.text(line1)
st.text(line2)

#PERTANYAAN 3
st.subheader('Berapa rata-rata pengguna bike rental setiap tahunnya dan mana yang mendominasi? (Casual atau Registered)')

# Memfilter data untuk tahun 2011
data_2011 = data[data['Year'] == 2011]

# Hitung total pengguna Casual dan Registered tahun 2011
total_casual = data_2011['Casual_User'].sum()
total_registered = data_2011['Registered_User'].sum()

# Buat pie chart untuk distribusi pengguna Casual dan Registered pada tahun 2011
labels_2011 = ['Casual', 'Registered']
sizes_2011 = [total_casual, total_registered]
colors_2011 = ['lightblue', 'orange']

plt.figure(figsize=(12, 6))

# Subplot untuk tahun 2011
plt.subplot(1, 2, 1)
plt.pie(sizes_2011, labels=labels_2011, autopct='%1.1f%%', colors=colors_2011)
plt.title('Distribusi Pengguna Casual dan Registered\nTahun 2011')


# Memfilter data untuk tahun 2012
data_2012 = data[data['Year'] == 2012]

# Hitung total pengguna Casual dan Registered tahun 2012
total_casual_2012 = data_2012['Casual_User'].sum()
total_registered_2012 = data_2012['Registered_User'].sum()

# Buat pie chart untuk distribusi pengguna Casual dan Registered pada tahun 2012
labels_2012 = ['Casual', 'Registered']
sizes_2012 = [total_casual_2012, total_registered_2012]
colors_2012 = ['green', 'lightcoral']

# Subplot untuk tahun 2012
plt.subplot(1, 2, 2)
plt.pie(sizes_2012, labels=labels_2012, autopct='%1.1f%%', colors=colors_2012)
plt.title('Distribusi Pengguna Casual dan Registered\nTahun 2012')

plt.tight_layout()
st.pyplot()

# Groupby berdasarkan tahun dan menghitung rata-rata pengguna Registered dan Casual
average_users_by_year = data.groupby('Year')[['Registered_User', 'Casual_User']].mean().reset_index()

# Membuat line plot untuk rata-rata pengguna Registered dan Casual pada tiap tahun
plt.figure(figsize=(10, 6))
sns.lineplot(x='Year', y='Registered_User', data=average_users_by_year, marker='o', label='Registered')
sns.lineplot(x='Year', y='Casual_User', data=average_users_by_year, marker='o', label='Casual')
plt.title('Rata-rata Pengguna Registered dan Casual pada Tiap Tahun')
plt.xlabel('Tahun')
plt.ylabel('Rata-rata Pengguna')
plt.legend()
st.pyplot()

# Menampilkan rata-ratanya
st.text("Rata-rata Pengguna Registered dan Casual pada Tiap Tahun:")
st.dataframe(average_users_by_year)

st.text("Rata-rata pengguna bike rental setiap tahunnya dapat dilihat pada output di atas. Visualisasi tersebut menunjukkan bahwa dari tahun ke tahun, pengguna Regitered memiliki kenaikan yang signifikan dan sangat mendominasi distribusi dari jenis pengguna")

st.subheader('Jadi, dapat diperkirakan bisnis rental bike akan memiliki tingkat kesuksesan yang tinggi pada musim gugur. Karena saat musim gugur, jumlah pengguna atau customer akan meningkat dengan signifikan.')