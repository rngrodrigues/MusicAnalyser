from tkinterdnd2 import TkinterDnD, DND_FILES
import tkinter as tk
from tkinter import ttk
import threading
import sys
import os

from interface.modal_help import abrir_help
from interface.modal_saiba_mais import abrir_saiba_mais
from core.data_loader import carregar_arquivo
from core.data_processing import processar_dados
from interface.close_window import finalizar
from interface.result_window import ResultWindow

# -----------------------------
# Função para PyInstaller
# -----------------------------
def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class MainWindow:
    def __init__(self):
        # -----------------------------
        # Janela principal
        # -----------------------------
        self.root = TkinterDnD.Tk()
        self.root.title("MusicAnalyser")

        # -----------------------------
        # Ícone da janela Tkinter
        # -----------------------------
        icon_path = resource_path("musica.ico")
        self.root.iconbitmap(icon_path)

        # -----------------------------
        # Centralizar tela
        # -----------------------------
        largura, altura = 1280, 720
        largura_tela = self.root.winfo_screenwidth()
        altura_tela = self.root.winfo_screenheight()
        pos_x = (largura_tela // 2) - (largura // 2)
        pos_y = (altura_tela // 2) - (altura // 2)
        self.root.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

        self.root.protocol("WM_DELETE_WINDOW", lambda: finalizar(self.root))

        self.progress = None

        # -----------------------------
        # Layouts
        # -----------------------------
        self.criar_layout_esquerda()
        self.criar_layout_direita()

    # --------------------------------------------------
    # LAYOUT ESQUERDA
    # --------------------------------------------------
    def criar_layout_esquerda(self):
        frame_esquerda = tk.Frame(self.root, bg="#0040FF")
        frame_esquerda.pack(side="left", expand=True, fill="both")

        conteudo = tk.Frame(frame_esquerda, bg="#0040FF")
        conteudo.place(relx=0.05, rely=0.5, anchor="w")

        linha = tk.Frame(conteudo, bg="white", width=3, height=200)
        linha.pack(side="left", fill="y", padx=(0, 15))

        texto_frame = tk.Frame(conteudo, bg="#0040FF")
        texto_frame.pack(side="left")

        tk.Label(
            texto_frame,
            text="Bem-vindo ao Music Analyser!",
            font=("Segoe UI", 18, "bold"),
            fg="white",
            bg="#0040FF"
        ).pack(anchor="w", pady=30)

        descricao = (
            " O Music Analyser é um projeto que permite explorar\n"
            "e entender melhor como funciona o mundo musical\n"
            "por meio de análise eficiente de grandes volumes de dados.\n\n"
            " Visualize as músicas mais populares de cada gênero\n"
            "de forma rápida e otimizada, garantindo alto\n"
            "desempenho mesmo ao lidar com arquivos de grande porte."
        )

        tk.Label(
            texto_frame,
            text=descricao,
            font=("Segoe UI", 12),
            fg="white",
            bg="#0040FF",
            justify="left"
        ).pack(anchor="w")

        link = tk.Label(
            texto_frame,
            text="Saiba mais",
            fg="white",
            bg="#0040FF",
            font=("Segoe UI", 12, "underline bold"),
            cursor="hand2"
        )
        link.pack(anchor="w", pady=30)
        link.bind("<Button-1>", lambda e: abrir_saiba_mais(self.root))

    # --------------------------------------------------
    # LAYOUT DIREITA
    # --------------------------------------------------
    def criar_layout_direita(self):
        frame_direita = tk.Frame(self.root, bg="white")
        frame_direita.pack(side="right", expand=True, fill="both")

        tamanho = 450
        canvas = tk.Canvas(
            frame_direita,
            width=tamanho,
            height=tamanho,
            bg="white",
            highlightthickness=0
        )
        canvas.place(relx=0.5, rely=0.5, anchor="center")

        margem = 10
        canvas.create_rectangle(
            margem, margem,
            tamanho - margem, tamanho - margem,
            dash=(6, 4),
            outline="#0040FF",
            width=2,
            tags="borda"
        )

        conteudo = tk.Frame(canvas, bg="white")
        canvas.create_window(
            tamanho / 2,
            tamanho / 2,
            window=conteudo,
            anchor="center"
        )

        botao = tk.Button(
            conteudo,
            text="Selecionar arquivo",
            command=self.carregar_dados,
            bg="#0040FF",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            padx=20,
            pady=10,
            relief="flat",
            cursor="hand2"
        )
        botao.pack(pady=(10, 8))

        tk.Label(
            conteudo,
            text="Ou solte arquivos aqui",
            fg="#0040FF",
            bg="white",
            font=("Segoe UI", 10, "italic")
        ).pack()

        link_como_usar = tk.Label(
            conteudo,
            text="Como usar?",
            fg="#0040FF",
            bg="white",
            font=("Segoe UI", 9, "underline bold"),
            cursor="hand2"
        )
        link_como_usar.pack(pady=5)
        link_como_usar.bind("<Button-1>", lambda e: abrir_help(self.root))

        canvas.drop_target_register(DND_FILES)
        canvas.dnd_bind("<<Drop>>", self.ao_soltar_arquivo)

    # --------------------------------------------------
    # EVENTOS
    # --------------------------------------------------
    def ao_soltar_arquivo(self, event):
        caminho = event.data.strip("{}")
        caminho = carregar_arquivo(caminho)
        if caminho:
            self.iniciar_processamento(caminho)

    def carregar_dados(self):
        caminho = carregar_arquivo()
        if caminho:
            self.iniciar_processamento(caminho)

    # --------------------------------------------------
    # PROCESSAMENTO (THREAD)
    # --------------------------------------------------
    def iniciar_processamento(self, caminho_arquivo):
        if self.progress:
            return

        self.progress = ttk.Progressbar(
            self.root,
            orient="horizontal",
            length=400,
            mode="determinate"
        )
        self.progress.place(relx=0.5, rely=0.9, anchor="center")
        self.progress["value"] = 0

        thread = threading.Thread(
            target=self.processar_em_background,
            args=(caminho_arquivo,),
            daemon=True
        )
        thread.start()

    def processar_em_background(self, caminho_arquivo):
        top10, generos = processar_dados(
            caminho_arquivo,
            progress_bar=self.progress,
            root=self.root
        )

        self.root.after(
            0,
            lambda: self.finalizar_processamento(top10, generos)
        )

    def finalizar_processamento(self, top10, generos):
        if self.progress:
            self.progress.destroy()
            self.progress = None

        if top10 is None:
            return

        ResultWindow(
            self.root,
            top10,
            generos,
            self.carregar_dados
        )

    # --------------------------------------------------
    def run(self):
        self.root.mainloop()
