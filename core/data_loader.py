from tkinter import filedialog, messagebox
import os

EXTENSOES_SUPORTADAS = {".csv", ".tsv", ".xlsx", ".xls", ".json", ".parquet"}

def carregar_arquivo(caminho=None):
    if caminho:
        caminho_arquivo = caminho
    else:
        caminho_arquivo = filedialog.askopenfilename(
            title="Selecione o arquivo de dados",
            filetypes=[
                ("Arquivos de dados", "*.csv *.tsv *.xlsx *.xls *.json *.parquet"),
                ("Todos", "*.*")
            ]
        )

    if not caminho_arquivo:
        messagebox.showinfo("Aviso", "Nenhum arquivo selecionado.")
        return None

    # Pega a extensão final, remove espaços, converte para minúsculo
    ext = os.path.splitext(caminho_arquivo)[1].strip().lower()

    if ext not in EXTENSOES_SUPORTADAS:
        messagebox.showerror(
            "Erro",
            f"Formato de arquivo não suportado: {ext}"
        )
        return None

    return caminho_arquivo
