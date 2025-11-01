import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, filedialog, messagebox


# 1. Carrega o dataset

caminho_arquivo = filedialog.askopenfilename(
    title="Selecione o arquivo CSV",
    filetypes=[("Arquivos CSV", "*.csv"), ("Todos os arquivos", "*.*")]
)

if not caminho_arquivo:
    messagebox.showerror("Erro", "Nenhum arquivo selecionado. O programa será encerrado.")
    exit()

try:
    df = pd.read_csv(caminho_arquivo)
except Exception as e:
    messagebox.showerror("Erro", f"Não foi possível ler o arquivo:\n{e}")
    exit()
# Verifica se as colunas necessárias existem
cols_necessarias = ['genre', 'track_name', 'popularity']
if not all(col in df.columns for col in cols_necessarias):
    messagebox.showerror("Erro", f"O arquivo precisa conter as colunas: {cols_necessarias}")
    exit()

df = df[cols_necessarias]
# Pega top 10 músicas de cada gênero
top10_por_genero = (
    df.groupby('genre', group_keys=False)
      .apply(lambda x: x.sort_values('popularity', ascending=False).head(10))
      .reset_index(drop=True)
)
# Lista de gêneros disponíveis
generos = sorted(top10_por_genero['genre'].unique())
# 2. Função para desenhar o gráfico
def atualizar_grafico(event):
    genero = combo_generos.get()
    top10_genero = top10_por_genero[top10_por_genero['genre'] == genero]
    ax.clear()
    ax.barh(top10_genero['track_name'], top10_genero['popularity'], color='skyblue')
    ax.set_xlabel('Popularidade')
    ax.set_title(f'Top 10 músicas mais populares de {genero}')
    ax.invert_yaxis()
    canvas.draw()

# 3. Cria a janela Tkinter

root = tk.Tk()
root.title("Top 10 Músicas por Gênero")

combo_generos = ttk.Combobox(root, values=generos)
combo_generos.current(0)
combo_generos.bind("<<ComboboxSelected>>", atualizar_grafico)
combo_generos.pack(pady=10)

fig, ax = plt.subplots(figsize=(10, 6))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()


atualizar_grafico(None)

root.mainloop()