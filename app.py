import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Load dataset menggunakan file uploader
uploaded_file = st.sidebar.file_uploader("Unggah file Excel", type=["xlsx"])
if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"Gagal memuat file Excel. Error: {e}")
        st.stop()
else:
    st.warning("Silakan unggah file Excel untuk melihat data.")
    st.stop()

# Pastikan kolom yang diperlukan ada di dataframe
required_columns = {'team', 'latitude', 'longitude', 'cluster'}
if not required_columns.issubset(df.columns):
    st.error(f"File Excel harus memiliki kolom berikut: {', '.join(required_columns)}")
    st.stop()

# Cek tipe data latitude dan longitude, konversi jika diperlukan
df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')

# Hilangkan baris dengan nilai NaN di latitude atau longitude
df.dropna(subset=['latitude', 'longitude'], inplace=True)

# Warna untuk cluster
cluster_colors = {0: 'blue', 1: 'green', 2: 'red'}
cluster_descriptions = {
    0: "Performa buruk",
    1: "Performa sedang",
    2: "Performa baik"
}

# Sidebar filter
st.sidebar.title("Filter")
selected_cluster = st.sidebar.multiselect(
    "Pilih Cluster", 
    options=df['cluster'].unique(), 
    default=df['cluster'].unique()
)

# Filter data berdasarkan cluster yang dipilih
filtered_df = df[df['cluster'].isin(selected_cluster)]

# Header aplikasi
st.title("Visualisasi Cluster Performa Tim Sepak Bola")
st.markdown(
    """
    Aplikasi ini menampilkan visualisasi peta interaktif dari tim sepak bola berdasarkan cluster performa.
    Warna marker:
    - **Blue**: Performa rendah
    - **Green**: Performa sedang
    - **Red**: Performa tinggi
    """
)

# Peta interaktif menggunakan Folium
if not filtered_df.empty:
    # Cek apakah data yang difilter memiliki latitude dan longitude yang valid
    if filtered_df['latitude'].notnull().any() and filtered_df['longitude'].notnull().any():
        m = folium.Map(location=[filtered_df['latitude'].mean(), filtered_df['longitude'].mean()], zoom_start=5)
        
        # Tambahkan marker ke peta
        for _, row in filtered_df.iterrows():
            cluster = row['cluster']
            color = cluster_colors.get(cluster, 'gray')
            popup_text = (
                f"<b>Team:</b> {row['team']}<br>"
                f"<b>Cluster:</b> <span style='color:{color};'>Cluster {cluster}</span><br>"
                f"<b>Latitude:</b> {row['latitude']}<br>"
                f"<b>Longitude:</b> {row['longitude']}"
            )
            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=8,
                color=color,
                fill=True,
                fill_opacity=0.7,
                popup=folium.Popup(popup_text, max_width=250)
            ).add_to(m)
        
        # Tampilkan peta di Streamlit
        st_folium(m, width=700, height=500)
    else:
        st.warning("Data yang tersedia tidak memiliki lokasi latitude atau longitude yang valid.")
else:
    st.warning("Tidak ada data untuk cluster yang dipilih.")

# Tabel data
st.subheader("Detail Data Tim Sepak Bola")
st.dataframe(filtered_df[['team', 'latitude', 'longitude', 'cluster']])
