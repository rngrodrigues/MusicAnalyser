import tkinter as tk
from interface.modal_help import abrir_modal
from core.data_loader import carregar_arquivo
from core.data_processing import processar_dados
from interface.close_window import finalizar
from interface.result_window import ResultWindow

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MusicAnalyser")
        self.root.geometry("900x600")
        self.root.config(bg="white")
        self.root.protocol("WM_DELETE_WINDOW", lambda: finalizar(self.root))

        self.criar_layout_esquerda()
        self.criar_layout_direita()

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
            texto_frame, text="Bem-vindo ao MusicAnalyser",
            font=("Segoe UI", 14, "bold"),
            fg="white", bg="#0040FF",
            justify="left", anchor="w"
        ).pack(anchor="w", pady=(10))

        descricao = (
                "Primeira frase do texto, apenas decorativo ainda.\n"
                "Segunda frase do texto, apenas decorativo ainda\n"
                "Terceira frase do texto, apenas decorativo ainda;\n\n"
                "É necessário conter as colunas:\n"
                "É necessário conter as colunas: É necessário conteraslunas:\n"
                "popularidade, nome e gênero. popularidade, ênero.populari.\n"
        )
        tk.Label(
            texto_frame, text=descricao,
            font=("Segoe UI", 10), fg="white", bg="#0040FF",
            justify="left", anchor="w"
        ).pack(anchor="w")

        link = tk.Label(
            texto_frame, text="Como usar?",
            fg="white", bg="#0040FF",
            font=("Segoe UI", 9, "underline bold"),
            cursor="hand2"
        )
        link.pack(anchor="w", pady=10)
        link.bind("<Button-1>", lambda e: abrir_modal(self.root))

    def criar_layout_direita(self):
        frame_direita = tk.Frame(self.root, bg="white")
        frame_direita.pack(side="right", expand=True, fill="both")

        # Botão Selecionar arquivo
        botao = tk.Button(
            frame_direita, text="Selecionar arquivo",
            command=self.carregar_dados,
            bg="#0040FF", fg="white",
            font=("Segoe UI", 10, "bold"),
            padx=20, pady=10, relief="flat",
            activebackground="#0030CC", activeforeground="white",
            cursor="hand2"
        )
        botao.place(relx=0.5, rely=0.5, anchor="center")  # 100% centralizado
        botao.bind("<Enter>", lambda e: botao.config(bg="#0030CC"))
        botao.bind("<Leave>", lambda e: botao.config(bg="#0040FF"))

        # Link "Como usar?" logo abaixo do botão
        link_como_usar = tk.Label(
            frame_direita, text="Como usar?",
            fg="#0040FF", bg="white",
            font=("Segoe UI", 9, "underline bold"),
            cursor="hand2"
        )
        link_como_usar.place(relx=0.5, rely=0.5 + 0.06, anchor="center")
        link_como_usar.bind("<Button-1>", lambda e: abrir_modal(self.root))

    def carregar_dados(self):
        df = carregar_arquivo()
        if df is None:
            return

        top10_por_genero, generos = processar_dados(df)
        if top10_por_genero is None:
            return

        ResultWindow(self.root, top10_por_genero, generos, self.carregar_dados)

    def run(self):
        self.root.mainloop()
