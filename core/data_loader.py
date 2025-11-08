from tkinter import filedialog, messagebox
import os
import pandas as pd
from core.data_cleaner import limpar_dados

def carregar_arquivo(caminho=None):
    # Se a função for chamada com um caminho direto (ex: arrastar e soltar)
    if caminho:
        caminho_arquivo = caminho
    else:
        # Abre o seletor de arquivos normalmente
        caminho_arquivo = filedialog.askopenfilename(
            title="Selecione o arquivo de dados",
            filetypes=[
                ("Todos arquivos de dados", "*.csv *.tsv *.xlsx *.xls *.json *.parquet"),
                ("CSV", "*.csv"),
                ("TSV", "*.tsv"),
                ("Excel", "*.xlsx *.xls"),
                ("JSON", "*.json"),
                ("Parquet", "*.parquet"),
                ("Todos", "*.*")
            ]
        )

    # 🔹 Se o usuário clicar em "Cancelar"
    if not caminho_arquivo:
        messagebox.showinfo("Aviso", "Nenhum arquivo selecionado.")
        return None

    # 🔹 Identifica a extensão do arquivo
    ext = os.path.splitext(caminho_arquivo)[1].lower()

    try:
        if ext == ".csv":
            df = pd.read_csv(caminho_arquivo)
        elif ext == ".tsv":
            df = pd.read_csv(caminho_arquivo, sep="\t")
        elif ext in [".xlsx", ".xls"]:
            df = pd.read_excel(caminho_arquivo)
        elif ext == ".json":
            df = pd.read_json(caminho_arquivo, lines=False)
        elif ext == ".parquet":
            df = pd.read_parquet(caminho_arquivo)
        else:
            messagebox.showerror("Erro", f"Formato de arquivo não suportado: {ext}")
            return None

        df = limpar_dados(df)

    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível ler o arquivo:\n{e}")
        return None

    return df
