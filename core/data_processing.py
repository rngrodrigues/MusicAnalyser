import pandas as pd
from tkinter import messagebox

def processar_dados(df, progress_bar=None, root=None):
    # Dicionário de colunas esperadas
    cols_necessarias = {
        "genre": ["genre", "genero", "style", "type", "song_type", "genre_id", "category", "music_type"],
        "music_name": ["music_name", "track_name", "track", "song", "song_name", "title_music", "name_music", "title", "music_title"],
        "popularity": ["popularity", "pop", "score", "ranking", "rank", "hits", "chart_position", "rating", "play_count"]
    }

    # Número de etapas do processo (ajuste conforme o número de passos que quiser representar)
    etapas = 6
    etapa_atual = 0

    def atualizar_barra():
        nonlocal etapa_atual
        etapa_atual += 1
        if progress_bar:
            progress_bar["value"] = (etapa_atual / etapas) * 100
            root.update_idletasks()  # atualiza a interface

    df_cols = [c.lower() for c in df.columns]

    # Etapa 1: Verifica colunas
    atualizar_barra()
    col_map = {}
    for key, options in cols_necessarias.items():
        for col in options:
            if col.lower() in df_cols:
                col_map[key] = df.columns[df_cols.index(col.lower())]
                break
        else:
            messagebox.showerror("Erro", f"O arquivo precisa conter uma coluna para '{key}' entre: {options}")
            return None, None

    # Etapa 2: Renomeia colunas
    atualizar_barra()
    df = df.rename(columns={
        col_map['genre']: 'genre',
        col_map['music_name']: 'track_name',
        col_map['popularity']: 'popularity'
    })

    # Etapa 3: Converte popularidade
    atualizar_barra()
    df['popularity'] = pd.to_numeric(df['popularity'], errors='coerce')

    # Etapa 4: Remove nulos
    atualizar_barra()
    df = df.dropna(subset=['genre', 'track_name', 'popularity'])

    # Etapa 5: Ordena e agrupa
    atualizar_barra()
    df_sorted = df.sort_values(['genre', 'popularity'], ascending=[True, False])
    top10_por_genero = df_sorted.groupby('genre').head(10).reset_index(drop=True)

    # Etapa 6: Gera lista de gêneros
    atualizar_barra()
    generos = sorted(top10_por_genero['genre'].unique().tolist())

    # Finaliza a barra
    if progress_bar:
        progress_bar["value"] = 100
        root.update_idletasks()

    return top10_por_genero, generos