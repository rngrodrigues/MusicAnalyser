import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from core.data_loader import carregar_arquivo
from core.data_processing import processar_dados

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Top 10 Músicas por Gênero")

        # Carrega arquivo (agora com PySpark)
        self.df = carregar_arquivo()
        if self.df is None:
            return

        # Processa dados (PySpark → Pandas)
        self.top10_por_genero, self.generos = processar_dados(self.df)
        if self.top10_por_genero is None:
            return

        # ComboBox
        self.combo_generos = ttk.Combobox(self.root, values=self.generos)
        self.combo_generos.current(0)
        self.combo_generos.bind("<<ComboboxSelected>>", self.atualizar_grafico)
        self.combo_generos.pack(pady=10)

        # Gráfico
        import matplotlib.pyplot as plt
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack()

        self.atualizar_grafico()

    def atualizar_grafico(self, event=None):
        genero = self.combo_generos.get()
        top10_genero = self.top10_por_genero[self.top10_por_genero['genre'] == genero]
        self.ax.clear()
        self.ax.barh(top10_genero['track_name'], top10_genero['popularity'], color='skyblue')
        self.ax.set_xlabel('Popularidade')
        self.ax.set_title(f'Top 10 músicas mais populares de {genero}')
        self.ax.invert_yaxis()
        self.canvas.draw()

    def run(self):
        self.root.mainloop()
