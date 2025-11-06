import pandas as pd
from tkinter import messagebox

def processar_dados(df):
    cols_necessarias = {
        "genre": ["genre", "genero", "style", "type", "song_type", "genre_id", "category", "music_type"],
        "music_name": ["music_name", "track_name", "track", "song", "song_name", "title_music", "name_music", "title", "music_title"],
        "popularity": ["popularity", "pop", "score", "ranking", "rank", "hits", "chart_position", "rating", "play_count"]
    }

    col_map = {}
    df_cols = [c.lower() for c in df.columns]

    for key, options in cols_necessarias.items():
        for col in options:
            if col.lower() in df_cols:
                col_map[key] = df.columns[df_cols.index(col.lower())]
                break
        else:
            messagebox.showerror("Erro", f"O arquivo precisa conter uma coluna para '{key}' entre: {options}")
            return None, None

    # Seleciona e renomeia colunas
    df = df.rename(columns={
        col_map['genre']: 'genre',
        col_map['music_name']: 'track_name',
        col_map['popularity']: 'popularity'
    })

    # Converte popularidade pra float
    df['popularity'] = pd.to_numeric(df['popularity'], errors='coerce')

    # Remove valores nulos
    df = df.dropna(subset=['genre', 'track_name', 'popularity'])

    # Agrupa e pega top 10 por gênero
    df_sorted = df.sort_values(['genre', 'popularity'], ascending=[True, False])
    top10_por_genero = df_sorted.groupby('genre').head(10).reset_index(drop=True)

    # Lista de gêneros
    generos = sorted(top10_por_genero['genre'].unique().tolist())

    return top10_por_genero, generos
