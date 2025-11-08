from tkinterdnd2 import TkinterDnD, DND_FILES
import tkinter as tk
from tkinter import ttk
from interface.modal_help import abrir_help
from interface.modal_saiba_mais import abrir_saiba_mais
from core.data_loader import carregar_arquivo
from core.data_processing import processar_dados
from interface.close_window import finalizar
from interface.result_window import ResultWindow

class MainWindow:
    def __init__(self):
        self.root = TkinterDnD.Tk()
        self.root.title("MusicAnalyser")
        largura, altura = 1280, 720
        largura_tela = self.root.winfo_screenwidth()
        altura_tela = self.root.winfo_screenheight()
        # Calcula posição para centralizar
        pos_x = (largura_tela // 2) - (largura // 2)
        pos_y = (altura_tela // 2) - (altura // 2)
        # Define posição centralizada
        self.root.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

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
            texto_frame, text="Bem-vindo ao Music Analyser!",
            font=("Segoe UI", 18, "bold"),
            fg="white", bg="#0040FF",
            justify="left", anchor="w"
        ).pack(anchor="w", pady=30)

        descricao = (
            " O Music Analyser é um projeto que permite explorar\n"
            "e entender melhor como funciona o mundo \n"
            "músical, por meio de uma análise inteligente dos dados.\n\n"
            " Ele oferece uma forma simples e interativa de\n"
            "visualizar as músicas mais populares por gênero,\n"
            "para descobrir padrões e ter insights valiosos!"
        )
        tk.Label(
            texto_frame, text=descricao,
            font=("Segoe UI", 12), fg="white", bg="#0040FF",
            justify="left", anchor="w"
        ).pack(anchor="w")

        link = tk.Label(
            texto_frame, text="Saiba mais",
            fg="white", bg="#0040FF",
            font=("Segoe UI", 12, "underline bold"),
            cursor="hand2"
        )
        link.pack(anchor="w", pady=30)
        link.bind("<Button-1>", lambda e: abrir_saiba_mais(self.root))

    def criar_layout_direita(self):
        frame_direita = tk.Frame(self.root, bg="white")
        frame_direita.pack(side="right", expand=True, fill="both")

        # 🔹 Canvas quadrado
        tamanho = 450  # ← aqui você controla o tamanho do quadrado
        canvas = tk.Canvas(
            frame_direita,
            width=tamanho, height=tamanho,
            bg="white",
            highlightthickness=0
        )
        canvas.place(relx=0.5, rely=0.5, anchor="center")

        # 🔹 Retângulo tracejado (quadrado)
        margem = 10
        canvas.create_rectangle(
            margem, margem,
            tamanho - margem, tamanho - margem,
            dash=(6, 4),
            outline="#0040FF",
            width=2,
            tags="borda"
        )

        # 🔹 Centraliza conteúdo no meio do quadrado
        conteudo = tk.Frame(canvas, bg="white")
        canvas.create_window(tamanho / 2, tamanho / 2, window=conteudo, anchor="center")

        # 🔹 Botão principal
        botao = tk.Button(
            conteudo, text="Selecionar arquivo",
            command=self.carregar_dados,
            bg="#0040FF", fg="white",
            font=("Segoe UI", 10, "bold"),
            padx=20, pady=10, relief="flat",
            activebackground="#0030CC", activeforeground="white",
            cursor="hand2"
        )
        botao.pack(pady=(10, 8))

        botao.bind("<Enter>", lambda e: botao.config(bg="#99BBFF"))
        botao.bind("<Leave>", lambda e: botao.config(bg="#0040FF"))

        # 🔹 Texto "(ou arraste aqui)"
        tk.Label(
            conteudo,
            text="Ou solte arquivos aqui",
            fg="#0040FF",
            bg="white",
            font=("Segoe UI", 10, "italic")
        ).pack(pady=(0, 5))

        # 🔹 Link "Como usar?"
        link_como_usar = tk.Label(
            conteudo,
            text="Como usar?",
            fg="#0040FF",
            bg="white",
            font=("Segoe UI", 9, "underline bold"),
            cursor="hand2"
        )
        link_como_usar.pack()
        link_como_usar.bind("<Button-1>", lambda e: abrir_help(self.root))

        canvas.drop_target_register(DND_FILES)
        # 🌀 Efeitos visuais ao arrastar arquivo
        def ao_entrar(event):
            # remove o tracejado e muda a cor pra azul clara
            canvas.itemconfig("borda", dash=(), outline="#0040FF", width=3)
        def ao_sair(event):
            # volta pro estilo original tracejado
            canvas.itemconfig("borda", dash=(6, 4), outline="#339CFF", width=2)
        # eventos de drag & drop
        canvas.dnd_bind("<<DropEnter>>", ao_entrar)
        canvas.dnd_bind("<<DropLeave>>", ao_sair)
        canvas.dnd_bind("<<Drop>>", self.ao_soltar_arquivo)

    def ao_soltar_arquivo(self, event):
            caminho_arquivo = event.data.strip("{}")  # remove chaves e espaços
            print("Arquivo recebido:", caminho_arquivo)

            # você pode reutilizar suas funções aqui:
            df = carregar_arquivo(caminho_arquivo)  # ajustar sua função pra aceitar caminho direto
            if df is None:
                return
            top10_por_genero, generos = processar_dados(df)
            if top10_por_genero is None:
                return
            ResultWindow(self.root, top10_por_genero, generos, self.carregar_dados)

    def carregar_dados(self):
        df = carregar_arquivo()
        if df is None:
            return

        # Cria a barra de progresso dentro da janela principal
        progress = ttk.Progressbar(
            self.root,
            orient="horizontal",
            length=400,
            mode="determinate"
        )
        progress.place(relx=0.5, rely=0.5, anchor="center")  # 🔹 exatamente no centro
        progress["value"] = 0
        self.root.update_idletasks()

        # Chama o processamento com barra
        top10_por_genero, generos = processar_dados(df, progress_bar=progress, root=self.root)

        # Remove a barra após o término
        progress.destroy()

        if top10_por_genero is None:
            return

        # Abre a janela de resultado
        ResultWindow(self.root, top10_por_genero, generos, self.carregar_dados)

    def run(self):
        self.root.mainloop()
