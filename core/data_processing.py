import duckdb
import os
import tempfile
import pandas as pd
from tkinter import messagebox

COLUNAS_ESPERADAS = {
    "genre": [
        "genre", "genero", "style", "type", "song_type", "genre_id", "category", "music_type"
    ],
    "music_name": [
        "music_name", "track_name", "track", "song", "song_name", "title_music", "name_music", "title", "music_title"
    ],
    "popularity": [
        "popularity", "pop", "score", "ranking", "rank", "chart_position", "rating", "play_count"
    ]
}

def processar_dados(caminho_arquivo, progress_bar=None, root=None):
    etapas = 6
    etapa_atual = 0

    def atualizar_barra():
        nonlocal etapa_atual
        etapa_atual += 1
        if progress_bar:
            progress_bar["value"] = (etapa_atual / etapas) * 100
            root.update_idletasks()

    # ------------------------------------------------
    # Conexão DuckDB em disco (spill automático)
    # ------------------------------------------------
    db_path = os.path.join(tempfile.gettempdir(), "musicas.duckdb")
    con = duckdb.connect(db_path)
    atualizar_barra()

    # ------------------------------------------------
    # Ler cabeçalho sem carregar tudo
    # ------------------------------------------------
    ext = os.path.splitext(caminho_arquivo)[1].lower()
    try:
        if ext in [".csv", ".tsv"]:
            sample = pd.read_csv(caminho_arquivo, nrows=5, sep="\t" if ext == ".tsv" else ",")
        elif ext in [".parquet"]:
            sample = pd.read_parquet(caminho_arquivo, engine="pyarrow")
        elif ext in [".json"]:
            # Detecta JSON array ou JSONL
            with open(caminho_arquivo, "r", encoding="utf-8") as f:
                first_char = f.read(1)
            if first_char == "[":
                sample = pd.read_json(caminho_arquivo, lines=False)
            else:
                sample = pd.read_json(caminho_arquivo, lines=True)
        else:
            messagebox.showerror("Erro", f"Formato não suportado: {ext}")
            return None, None
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao ler cabeçalho:\n{e}")
        return None, None

    # ------------------------------------------------
    # Mapear colunas
    # ------------------------------------------------
    df_cols = [c.lower() for c in sample.columns]
    col_map = {}
    for chave, opcoes in COLUNAS_ESPERADAS.items():
        for c in opcoes:
            if c.lower() in df_cols:
                col_map[chave] = sample.columns[df_cols.index(c.lower())]
                break
        else:
            messagebox.showerror("Erro", f"Coluna obrigatória não encontrada: '{chave}'")
            return None, None

    atualizar_barra()

    # ------------------------------------------------
    # Criar tabela DuckDB direto do arquivo
    # ------------------------------------------------
    con.execute("DROP TABLE IF EXISTS musicas_raw")

    if ext in [".csv", ".tsv"]:
        sep = "\t" if ext == ".tsv" else ","
        con.execute(f"""
            CREATE TABLE musicas_raw AS
            SELECT
                "{col_map['genre']}"       AS genre,
                "{col_map['music_name']}" AS track_name,
                TRY_CAST("{col_map['popularity']}" AS DOUBLE) AS popularity
            FROM read_csv_auto('{caminho_arquivo}', delim='{sep}')
            WHERE "{col_map['genre']}" IS NOT NULL
              AND "{col_map['music_name']}" IS NOT NULL
              AND "{col_map['popularity']}" IS NOT NULL
        """)
    elif ext == ".parquet":
        con.execute(f"""
            CREATE TABLE musicas_raw AS
            SELECT
                "{col_map['genre']}"       AS genre,
                "{col_map['music_name']}" AS track_name,
                TRY_CAST("{col_map['popularity']}" AS DOUBLE) AS popularity
            FROM parquet_scan('{caminho_arquivo}')
        """)
    elif ext == ".json":
        con.execute(f"""
            CREATE TABLE musicas_raw AS
            SELECT
                "{col_map['genre']}"       AS genre,
                "{col_map['music_name']}" AS track_name,
                TRY_CAST("{col_map['popularity']}" AS DOUBLE) AS popularity
            FROM read_json_auto('{caminho_arquivo}')
        """)
    else:
        messagebox.showerror("Erro", "Formato não suportado para processamento.")
        return None, None

    atualizar_barra()

    # ------------------------------------------------
    # Top 10 por gênero
    # ------------------------------------------------
    query = """
        SELECT genre, track_name, popularity
        FROM (
            SELECT genre, track_name, popularity,
                   ROW_NUMBER() OVER (PARTITION BY genre ORDER BY popularity DESC) AS rn
            FROM musicas_raw
        )
        WHERE rn <= 10
        ORDER BY genre, popularity DESC
    """
    atualizar_barra()

    top10 = con.execute(query).fetchdf()
    generos = sorted(top10["genre"].dropna().unique().tolist())

    if progress_bar:
        progress_bar["value"] = 100
        root.update_idletasks()

    return top10, generos
