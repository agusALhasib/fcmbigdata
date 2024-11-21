import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Load dataset menggunakan file uploader
uploaded_file = st.sidebar.file_uploader("Unggah file Excel", type=["xlsx"])
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
else:
    st.warning("Silakan unggah file Excel untuk melihat data.")
    st.stop()


# Warna untuk cluster
cluster_colors = {0: 'blue', 1: 'green', 2: 'red'}
cluster_descriptions = {
    0: "Performa rendah",
    1: "Performa sedang",
    2: "Performa tinggi"
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
    st.warning("Tidak ada data untuk cluster yang dipilih.")

# Tabel data
st.subheader("Detail Data Tim Sepak Bola")
st.dataframe(filtered_df[['team', 'latitude', 'longitude', 'cluster']])
