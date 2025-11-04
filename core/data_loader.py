from tkinter import filedialog, messagebox
import os
import pandas as pd
from core.spark_session import get_spark
from core.data_cleaner import limpar_dados

def carregar_arquivo():
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

    if not caminho_arquivo:
        messagebox.showerror("Erro", "Nenhum arquivo selecionado. O programa será encerrado.")
        return None

    ext = os.path.splitext(caminho_arquivo)[1].lower()

    try:
        spark = get_spark()

        # Leitura do arquivo conforme o tipo
        if ext == ".csv":
            df = (
                spark.read
                .option("header", "true")
                .option("inferSchema", "true")
                .option("multiLine", "true")
                .option("escape", '"')
                .option("quote", '"')
                .option("sep", ",")
                .csv(caminho_arquivo)
            )

        elif ext == ".tsv":
            df = (
                spark.read
                .option("header", "true")
                .option("sep", "\t")
                .csv(caminho_arquivo)
            )

        elif ext in [".xlsx", ".xls"]:
            try:
                pdf = pd.read_excel(caminho_arquivo)
                df = spark.createDataFrame(pdf)
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao ler o arquivo Excel:\n{e}")
                return None

        elif ext == ".json":
            df = spark.read.option("multiline", "true").json(caminho_arquivo)

        elif ext == ".parquet":
            df = spark.read.parquet(caminho_arquivo)

        else:
            messagebox.showerror("Erro", f"Formato de arquivo não suportado: {ext}")
            return None


        df = limpar_dados(df)

    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível ler o arquivo:\n{e}")
        return None

    return df
