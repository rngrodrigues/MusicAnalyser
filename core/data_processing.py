def processar_dados(df):
    cols_necessarias = {
        "genre": ["genre", "genero", "style", "type", "song_type", "genre_id", "category", "music_type"],
        "music_name": ["music_name", "track_name", "track", "song", "song_name", "title_music", "name_music", "title", "music_title"],
        "popularity": ["popularity", "pop", "score", "ranking", "rank", "hits", "chart_position", "rating", "play_count"]
    }

    col_map = {}
    for key, options in cols_necessarias.items():
        for col in options:
            if col in df.columns:
                col_map[key] = col
                break
        else:
            from tkinter import messagebox
            messagebox.showerror("Erro", f"O arquivo precisa conter uma coluna para '{key}' entre: {options}")
            return None, None

    df = df[[col_map['genre'], col_map['music_name'], col_map['popularity']]]
    df.columns = ['genre', 'track_name', 'popularity']

    top10_por_genero = (
        df.groupby('genre', group_keys=False)
          .apply(lambda x: x.sort_values('popularity', ascending=False).head(10))
          .reset_index(drop=True)
    )
    generos = sorted(top10_por_genero['genre'].unique())
    return top10_por_genero, generos
