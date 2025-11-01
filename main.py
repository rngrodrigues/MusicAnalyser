import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk

# -------------------------------
# 1. Carrega o dataset
# -------------------------------
df = pd.read_csv("dataset\SpotifyFeatures.csv")
cols = ['genre', 'track_name', 'artist_name', 'popularity']
df = df[cols]

# Pega top 10 músicas de cada gênero

top10_por_genero = (
    df.groupby('genre', group_keys=False)
      .apply(lambda x: x.sort_values('popularity', ascending=False).head(10))
      .reset_index(drop=True)
)

# Lista de gêneros disponíveis
generos = sorted(top10_por_genero['genre'].unique())

# -------------------------------
# 2. Função para desenhar o gráfico
# -------------------------------
def atualizar_grafico(event):
    genero = combo_generos.get()
    top10_genero = top10_por_genero[top10_por_genero['genre'] == genero]
    ax.clear()
    ax.barh(top10_genero['track_name'], top10_genero['popularity'], color='skyblue')
    ax.set_xlabel('Popularidade')
    ax.set_title(f'Top 10 músicas mais populares de {genero}')
    ax.invert_yaxis()
    canvas.draw()
# -------------------------------
# 3. Cria a janela Tkinter
# -------------------------------
root = tk.Tk()
root.title("Top 10 Músicas por Gênero")

combo_generos = ttk.Combobox(root, values=generos)
combo_generos.current(0)
combo_generos.bind("<<ComboboxSelected>>", atualizar_grafico)
combo_generos.pack(pady=10)

fig, ax = plt.subplots(figsize=(10, 6))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Desenha gráfico inicial
atualizar_grafico(None)

root.mainloop()