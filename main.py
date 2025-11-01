import os
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim, regexp_replace, initcap, row_number, desc, asc
from pyspark.sql.window import Window

# -------------------------------
# 1. Inicializa Spark
# -------------------------------
spark = (
    SparkSession.builder
    .appName("MusicAnalyser")
    .master("local[*]")
    .getOrCreate()
)

# -------------------------------
# 2. Função para ler arquivos
# -------------------------------
def ler_arquivo(caminho: str):
    ext = os.path.splitext(caminho)[1].lower()
    try:
        if ext in (".csv", ".tsv"):
            sep = "\t" if ext == ".tsv" else ","
            return spark.read.csv(caminho, header=True, inferSchema=True, sep=sep)
        elif ext in (".xls", ".xlsx"):
            return spark.createDataFrame(pd.read_excel(caminho))
        elif ext == ".json":
            return spark.read.json(caminho)
        elif ext == ".parquet":
            return spark.read.parquet(caminho)
        elif ext == ".feather":
            return spark.createDataFrame(pd.read_feather(caminho))
        else:
            raise ValueError(f"Formato de arquivo não suportado: {ext}")
    except Exception as e:
        raise ValueError(f"Erro ao ler o arquivo: {e}")

# -------------------------------
# 3. Interface principal
# -------------------------------

import tkinter as tk

root = tk.Tk()
root.title("MusicAnalyser")
root.geometry("900x600")
root.config(bg="white")

# --- LAYOUT DIVIDIDO ---
frame_esquerda = tk.Frame(root, bg="#0040FF")
frame_esquerda.pack(side="left", expand=True, fill="both")

frame_direita = tk.Frame(root, bg="white")
frame_direita.pack(side="right", expand=True, fill="both")

# --- CONTEÚDO À ESQUERDA ---
# Centraliza verticalmente e encosta à esquerda
conteudo = tk.Frame(frame_esquerda, bg="#0040FF")
conteudo.place(relx=0.05, rely=0.5, anchor="w")  # 0.05 = distância da borda esquerda, rely=0.5 centraliza verticalmente

# Linha branca
linha = tk.Frame(conteudo, bg="white", width=3, height=200)
linha.pack(side="left", fill="y", padx=(0, 15))

# Container de texto (título + descrição + link)
texto_frame = tk.Frame(conteudo, bg="#0040FF")
texto_frame.pack(side="left")

titulo = tk.Label(
    texto_frame,
    text="Bem-vindo ao MusicAnalyser",
    font=("Segoe UI", 14, "bold"),
    fg="white",
    bg="#0040FF",
    justify="left",
    anchor="w"
)
titulo.pack(anchor="w", pady=(10))

descricao = tk.Label(
    texto_frame,
    text="Análise de dados em formato CSV, Parquet, JSON.\n"
         "Análise de dados em formato CSV, Parquet, JSON.\n"
         "Análise de dados em formato CSV, Parquet, JSON.\n\n"
         "É necessário conter as colunas: \n"
         "É necessário conter as colunas: É necessário conteraslunas: \n"
         "popularidade, nome e gênero. popularidade, ênero.populari.\n",
    font=("Segoe UI", 10),
    fg="white",
    bg="#0040FF",
    justify="left",
    anchor="w"
)
descricao.pack(anchor="w")

# --- FUNÇÃO DO MODAL ---
def abrir_modal():
    modal = tk.Toplevel(root)
    modal.title("Como usar o MusicAnalyser")
    largura = 420
    altura = 260
    modal.geometry(f"{largura}x{altura}")
    modal.config(bg="white")
    modal.resizable(False, False)
    modal.transient(root)
    modal.grab_set()

    # Centraliza o modal em relação à janela principal
    root_x = root.winfo_x()
    root_y = root.winfo_y()
    root_largura = root.winfo_width()
    root_altura = root.winfo_height()

    pos_x = root_x + (root_largura // 2) - (largura // 2)
    pos_y = root_y + (root_altura // 2) - (altura // 2)

    modal.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

    label = tk.Label(
        modal,
        text=("Clique em 'Selecionar arquivo' para carregar seu dataset.\n\n"
              "O arquivo deve conter colunas como:\n"
              "- gênero (genre)\n"
              "- nome da música (track_name)\n"
              "- popularidade (popularity)\n\n"
              "Após carregar, selecione um gênero e veja o Top 10!"),
        bg="white",
        fg="black",
        justify="left",
        font=("Segoe UI", 10)
    )
    label.pack(padx=20, pady=20)

    tk.Button(
        modal,
        text="Fechar",
        command=modal.destroy,
        bg="#0040FF",
        fg="white",
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        padx=10,
        pady=5
    ).pack(pady=10)

# --- LINK "Como usar?" ---
link = tk.Label(
    texto_frame,
    text="Como usar?",
    fg="white",
    bg="#0040FF",
    font=("Segoe UI", 9, "underline bold"),
    cursor="hand2",
)
link.pack(anchor="w", pady=10)
link.bind("<Button-1>", lambda e: abrir_modal())

botao = tk.Button(
    frame_direita,
    text="Selecionar arquivo",
    command=lambda: carregar_dados(),
    bg="#0040FF",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    padx=20,
    pady=10,
    relief="flat",
    activebackground="#0030CC",
    activeforeground="white",
    cursor="hand2"
)
botao.place(relx=0.5, rely=0.5, anchor="center")

# Funções de hover
def on_enter(e):
    botao.config(bg="#0030CC")  # muda a cor ao passar o mouse

def on_leave(e):
    botao.config(bg="#0040FF")  # volta à cor original ao sair

# Bind dos eventos — fora de qualquer função
botao.bind("<Enter>", on_enter)
botao.bind("<Leave>", on_leave)


# -------------------------------
# 4. Função de carregar dados
# -------------------------------
def selecionar_arquivo():
    tipos = [
        ("Todos arquivos de dados", "*.csv *.tsv *.xlsx *.xls *.json *.parquet *.feather"),
        ("CSV", "*.csv"), ("TSV", "*.tsv"), ("Excel", "*.xlsx *.xls"),
        ("JSON", "*.json"), ("Parquet", "*.parquet"), ("Feather", "*.feather"),
        ("Todos", "*.*")
    ]
    return filedialog.askopenfilename(title="Selecione o arquivo", filetypes=tipos)

def carregar_dados():
    caminho = selecionar_arquivo()
    if not caminho:
        messagebox.showinfo("Aviso", "Nenhum arquivo selecionado.")
        return

    try:
        df_spark = ler_arquivo(caminho)
    except Exception as e:
        messagebox.showerror("Erro", str(e))
        return

    # Mapeamento de colunas
    col_map = {
        "genre": ["genre", "genero", "style", "type", "song_type", "genre_id"],
        "track_name": ["track_name", "track", "song", "song_name", "trackname", "music_title", "name"],
        "popularity": ["popularity", "pop", "score", "ranking"]
    }

    for novo, aliases in col_map.items():
        for c in df_spark.columns:
            if c.lower() in [a.lower() for a in aliases]:
                df_spark = df_spark.withColumnRenamed(c, novo)

    faltando = [c for c in col_map if c not in df_spark.columns]
    if faltando:
        messagebox.showerror("Erro", f"Colunas ausentes: {', '.join(faltando)}")
        return

    df_spark = (
        df_spark.select(*col_map.keys())
        .filter(col("popularity").isNotNull())
        .withColumn("genre", initcap(trim(regexp_replace(col("genre"), "[‘’]", "'"))))
        .withColumn("popularity", col("popularity").cast("int"))
    )

    window = Window.partitionBy("genre").orderBy(desc("popularity"))
    df_top10 = (
        df_spark.withColumn("rank", row_number().over(window))
        .filter(col("rank") <= 10)
        .select("genre", "track_name", "popularity")
        .orderBy(asc("genre"), desc("popularity"))
    )

    global top10_df, generos
    top10_df = df_top10.toPandas().sort_values(["genre", "popularity"], ascending=[True, False])
    generos = sorted(g for g in top10_df["genre"].unique() if g)

    abrir_tela_resultado()

# -------------------------------
# 5. Tela de gráfico
# -------------------------------
def abrir_tela_resultado():
    for widget in root.winfo_children():
        widget.destroy()

    frame_top = tk.Frame(root, bg="white")
    frame_top.pack(fill="x", pady=10)

    # Cria um frame para agrupar o botão e o link, alinhando-os verticalmente
    frame_botoes = tk.Frame(frame_top, bg="white")
    frame_botoes.pack(side="left", padx=20, pady=5)

    botao_alterar = tk.Button(
        frame_botoes,
        text="Alterar arquivo",
        command=lambda: carregar_dados(),
        bg="#0040FF",
        fg="white",
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        padx=10,
        pady=5,
        cursor="hand2"
    )
    botao_alterar.pack()  # Default pack é top (vertical)

    def on_enter_alterar(e):
        botao_alterar.config(bg="#0030CC")

    def on_leave_alterar(e):
        botao_alterar.config(bg="#0040FF")

    botao_alterar.bind("<Enter>", on_enter_alterar)
    botao_alterar.bind("<Leave>", on_leave_alterar)

    link_como_usar = tk.Label(
        frame_botoes,
        text="Como usar?",
        fg="#0040FF",
        bg="white",
        font=("Segoe UI", 9, "underline"),
        cursor="hand2"
    )
    link_como_usar.pack(pady=(5, 0))
    link_como_usar.bind("<Button-1>", lambda e: abrir_modal())

    combo_generos = ttk.Combobox(
        frame_top,
        values=generos,
        font=("Segoe UI", 10),
        justify="center",
    )
    combo_generos.pack(pady=(0, 10))  # centraliza horizontalmente e dá espaço abaixo do título
    combo_generos.current(0)

    fig, ax = plt.subplots(figsize=(10, 6))
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack(fill="both", expand=True)

    def atualizar_grafico(_=None):
        genero = combo_generos.get()
        dados = top10_df[top10_df["genre"] == genero].copy()
        dados["popularity"] = pd.to_numeric(dados["popularity"], errors="coerce")
        dados = dados.dropna(subset=["popularity"])

        ax.clear()

        # Cria o gráfico de barras
        bars = ax.barh(dados["track_name"], dados["popularity"], color="#4C8BFF", edgecolor="black", alpha=0.8)

        # Define os ticks do eixo Y corretamente
        ax.set_yticks(range(len(dados["track_name"])))
        ax.set_yticklabels(dados["track_name"], fontname="Yu Gothic", fontsize=10)

        # Adiciona os valores nas barras
        for bar in bars:
            w = bar.get_width()
            ax.text(w + 1, bar.get_y() + bar.get_height() / 2, f"{int(w)}", va="center", fontsize=10, fontweight="bold")

        # Configurações do gráfico
        ax.set(xlabel="Popularidade", ylabel="Música", title=f"Top 10 músicas mais populares de {genero}")
        ax.xaxis.grid(True, linestyle="--", alpha=0.5)
        ax.invert_yaxis()

        plt.tight_layout()
        canvas.draw()

    combo_generos.bind("<<ComboboxSelected>>", atualizar_grafico)
    atualizar_grafico()

# -------------------------------
# 6. Fechar corretamente
# -------------------------------


def finalizar():
    spark.stop()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", finalizar)
root.mainloop()
