import duckdb
from tkinter import messagebox

def processar_dados(df, progress_bar=None, root=None):
    # Dicionário de colunas esperadas
    cols_necessarias = {
        "genre": ["genre", "genero", "style", "type", "song_type", "genre_id", "category", "music_type"],
        "music_name": ["music_name", "track_name", "track", "song", "song_name", "title_music", "name_music", "title", "music_title"],
        "popularity": ["popularity", "pop", "score", "ranking", "rank", "hits", "chart_position", "rating", "play_count"]
    }

    etapas = 6
    etapa_atual = 0

    def atualizar_barra():
        nonlocal etapa_atual
        etapa_atual += 1
        if progress_bar:
            progress_bar["value"] = (etapa_atual / etapas) * 100
            root.update_idletasks()

    # Etapa 1: Verifica colunas
    atualizar_barra()
    df_cols = [c.lower() for c in df.columns]
    col_map = {}

    for key, options in cols_necessarias.items():
        for col in options:
            if col.lower() in df_cols:
                col_map[key] = df.columns[df_cols.index(col.lower())]
                break
        else:
            messagebox.showerror(
                "Erro",
                f"O arquivo precisa conter uma coluna para '{key}' entre: {options}"
            )
            return None, None

    # Etapa 2: Renomeia colunas
    atualizar_barra()
    df = df.rename(columns={
        col_map["genre"]: "genre",
        col_map["music_name"]: "track_name",
        col_map["popularity"]: "popularity"
    })

    # Etapa 3: Processamento com DuckDB
    atualizar_barra()
    con = duckdb.connect(database=":memory:")
    con.register("dados", df)

    query = """
        SELECT
            genre,
            track_name,
            CAST(popularity AS DOUBLE) AS popularity
        FROM dados
        WHERE genre IS NOT NULL
          AND track_name IS NOT NULL
          AND popularity IS NOT NULL
        QUALIFY
            ROW_NUMBER() OVER (
                PARTITION BY genre
                ORDER BY popularity DESC
            ) <= 10
        ORDER BY genre, popularity DESC
    """

    try:
        top10_por_genero = con.execute(query).df()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro no processamento dos dados:\n{e}")
        return None, None

    # Etapa 4: Gera lista de gêneros
    atualizar_barra()
    generos = sorted(top10_por_genero["genre"].unique().tolist())

    # Finaliza barra
    if progress_bar:
        progress_bar["value"] = 100
        root.update_idletasks()

    return top10_por_genero, generos
