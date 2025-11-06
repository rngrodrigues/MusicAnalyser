import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from interface.modal_help import abrir_help
from interface.close_window import finalizar
from matplotlib import rcParams, font_manager

# Caminhos para as fontes Noto
FONT_PATHS = {
    "default": r"fonts/NotoSans-VariableFont_wdth,wght.ttf",
    "arabic": r"fonts/NotoSansArabic-VariableFont_wdth,wght.ttf",
    "japanese": r"fonts/NotoSansJP-VariableFont_wght.ttf",
    "korean": r"fonts/NotoSansKR-VariableFont_wght.ttf",
    "simplified_chinese": r"fonts/NotoSansSC-VariableFont_wght.ttf"
}

# Registra todas as fontes
for path in FONT_PATHS.values():
    font_manager.fontManager.addfont(path)

# Configura fallback de fontes
rcParams['font.family'] = [
    'Noto Sans',
    'Noto Sans Arabic',
    'Noto Sans JP',
    'Noto Sans KR',
    'Noto Sans SC',
    'DejaVu Sans',  # fallback padrão
]

class ResultWindow:
    def __init__(self, root, top10_por_genero, generos, carregar_dados):
        self.root = root
        self.top10_por_genero = top10_por_genero
        self.generos = generos
        self.carregar_dados = carregar_dados

        # Remove conteúdo antigo
        for widget in self.root.winfo_children():
            widget.destroy()

        # Captura o clique no X
        self.root.protocol("WM_DELETE_WINDOW", lambda: finalizar(self.root))

        self.criar_layout()
        self.criar_grafico()
        self.atualizar_grafico()

    def criar_layout(self):
        # Frame superior e botões
        self.frame_top = tk.Frame(self.root, bg="white")
        self.frame_top.pack(fill="x", pady=10)

        self.frame_botoes = tk.Frame(self.frame_top, bg="white")
        self.frame_botoes.pack(side="left", padx=20, pady=5)

        # Botão Alterar arquivo
        self.botao_alterar = tk.Button(
            self.frame_botoes, text="Alterar arquivo",
            command=self.carregar_dados,
            bg="#0040FF", fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat", padx=10, pady=5, cursor="hand2"
        )
        self.botao_alterar.pack()
        self.botao_alterar.bind("<Enter>", lambda e: self.botao_alterar.config(bg="#0030CC"))
        self.botao_alterar.bind("<Leave>", lambda e: self.botao_alterar.config(bg="#0040FF"))

        # Link "Como usar"
        self.link_como_usar = tk.Label(
            self.frame_botoes, text="Como usar?",
            fg="#0040FF", bg="white",
            font=("Segoe UI", 9, "underline"),
            cursor="hand2"
        )
        self.link_como_usar.pack(pady=(5, 0))
        self.link_como_usar.bind("<Button-1>", lambda e: abrir_help(self.root))

        # ComboBox de gêneros
        self.combo_generos = ttk.Combobox(
            self.frame_top, values=self.generos,
            font=("Segoe UI", 10), justify="center"
        )
        self.combo_generos.pack(pady=(0, 10))
        self.combo_generos.current(0)

    def criar_grafico(self):
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        self.combo_generos.bind("<<ComboboxSelected>>", self.atualizar_grafico)

    def atualizar_grafico(self, event=None):
        genero = self.combo_generos.get()
        top10_genero = self.top10_por_genero[self.top10_por_genero['genre'] == genero]

        self.ax.clear()
        bars = self.ax.barh(
            top10_genero['track_name'],
            top10_genero['popularity'],
            color='#4C8BFF', edgecolor='black', alpha=0.8
        )

        self.ax.set_xlabel('Popularidade', fontsize=12)
        self.ax.set_ylabel('Música', fontsize=12)
        self.ax.set_title(f'Top 10 músicas mais populares de {genero}', fontsize=14)

        # Labels usando fallback das fontes Noto
        self.ax.set_yticks(range(len(top10_genero['track_name'])))
        self.ax.set_yticklabels(top10_genero['track_name'], fontsize=10)

        # Valores das barras
        for bar in bars:
            largura = bar.get_width()
            self.ax.text(largura + 1, bar.get_y() + bar.get_height() / 2,
                         f"{int(largura)}", va='center', fontsize=10, fontweight='bold')

        self.ax.xaxis.grid(True, linestyle="--", alpha=0.5)
        self.ax.invert_yaxis()
        plt.tight_layout()
        self.canvas.draw()
