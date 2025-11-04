from pyspark.sql import functions as F
from tkinter import messagebox
from pyspark.sql.window import Window

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
    df = df.select(
        F.col(col_map['genre']).alias('genre'),
        F.col(col_map['music_name']).alias('track_name'),
        F.col(col_map['popularity']).cast('float').alias('popularity')
    )

    window_spec = Window.partitionBy("genre").orderBy(F.desc("popularity"))
    df_ranked = df.withColumn("rank", F.row_number().over(window_spec))
    top10_por_genero = df_ranked.filter(F.col("rank") <= 10).drop("rank")

    # Lista de gêneros (coletar para o ComboBox)
    generos = [row["genre"] for row in top10_por_genero.select("genre").distinct().collect()]

    #  Converte o resultado para pandas no final (para o matplotlib e tkinter)
    top10_por_genero_pd = top10_por_genero.toPandas()


    return top10_por_genero_pd, sorted(generos)
