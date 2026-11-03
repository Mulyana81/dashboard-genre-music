
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Music Genre Dashboard", layout="wide")

st.title("🎵 Dashboard Analisis Genre Musik")
st.write("Dashboard interaktif untuk mengeksplorasi tren dan korelasi genre musik.")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv('music.csv')
    return df

try:
    df = load_data()
    
    # Sidebar filter
    st.sidebar.header("Filter Tahun")
    min_year, max_year = int(df['year'].min()), int(df['year'].max())
    year_range = st.sidebar.slider("Pilih Rentang Tahun", min_year, max_year, (1990, 2010))
    
    # Filter data berdasarkan tahun
    df_filtered = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]
    
    # Menampilkan data
    if st.checkbox("Tampilkan Data Mentah"):
        st.dataframe(df_filtered.head(100))
        
    # Tab untuk visualisasi
    tab1, tab2 = st.tabs(["📈 Tren Genre", "🔥 Korelasi Genre"])
    
    with tab1:
        st.subheader("Tren Perkembangan Genre Musik")
        # Proses data genre
        df_genres = df_filtered.copy()
        df_genres['genres'] = df_genres['genres'].str.split('|')
        df_genres = df_genres.explode('genres')
        
        top_genres = df_genres['genres'].value_counts().head(5).index
        df_top = df_genres[df_genres['genres'].isin(top_genres)].copy()
        df_top['year_bin'] = (df_top['year'] // 5) * 5
        trend_data = df_top.groupby(['year_bin', 'genres']).size().unstack(fill_value=0)
        
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.lineplot(data=trend_data, dashes=False, marker='o', ax=ax)
        plt.xticks(trend_data.index, rotation=45)
        st.pyplot(fig)
        
    with tab2:
        st.subheader("Korelasi Antar Genre")
        genre_dummies = df_filtered['genres'].str.get_dummies(sep='|')
        genre_corr = genre_dummies.corr()
        
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(genre_corr, annot=True, cmap='coolwarm', fmt='.2f', ax=ax)
        st.pyplot(fig)

except Exception as e:
    st.error(f"Silakan unggah file 'music.csv' bersama dengan script ini di repositori GitHub Anda. Error: {e}")
