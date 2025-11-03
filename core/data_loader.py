import pandas as pd
from tkinter import filedialog, messagebox
import os

def carregar_arquivo():
    caminho_arquivo = filedialog.askopenfilename(
        title="Selecione o arquivo de dados",
        filetypes=[
            ("Todos arquivos de dados", "*.csv *.tsv *.xlsx *.xls *.json *.parquet *.feather"),
            ("CSV", "*.csv"),
            ("TSV", "*.tsv"),
            ("Excel", "*.xlsx *.xls"),
            ("JSON", "*.json"),
            ("Parquet", "*.parquet"),
            ("Feather", "*.feather"),
            ("Todos", "*.*")
        ]
    )

    if not caminho_arquivo:
        messagebox.showerror("Erro", "Nenhum arquivo selecionado. O programa será encerrado.")
        return None

    ext = os.path.splitext(caminho_arquivo)[1].lower()

    try:
        if ext == ".csv":
            df = pd.read_csv(caminho_arquivo)
        elif ext == ".tsv":
            df = pd.read_csv(caminho_arquivo, sep="\t")
        elif ext in [".xlsx", ".xls"]:
            df = pd.read_excel(caminho_arquivo)
        elif ext == ".json":
            df = pd.read_json(caminho_arquivo)
        elif ext == ".parquet":
            df = pd.read_parquet(caminho_arquivo)
        elif ext == ".feather":
            df = pd.read_feather(caminho_arquivo)
        else:
            messagebox.showerror("Erro", "Formato de arquivo não suportado.")
            return None
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível ler o arquivo:\n{e}")
        return None

    return df
