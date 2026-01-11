import tkinter as tk

def abrir_help(parent):
    modal = tk.Toplevel(parent)
    modal.title("Como usar o MusicAnalyser")
    largura, altura = 420, 300
    modal.geometry(f"{largura}x{altura}")
    modal.config(bg="white")
    modal.resizable(False, False)
    modal.transient(parent)
    modal.grab_set()

    # Centraliza o modal
    root_x = parent.winfo_x()
    root_y = parent.winfo_y()
    root_largura = parent.winfo_width()
    root_altura = parent.winfo_height()
    pos_x = root_x + (root_largura // 2) - (largura // 2)
    pos_y = root_y + (root_altura // 2) - (altura // 2)
    modal.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

    # Título centralizado
    tk.Label(
        modal,
        text="Music Analyser",
        bg="white",
        fg="#0040FF",
        font=("Segoe UI", 14, "bold")
    ).pack(pady=(15, 5))

    # Conteúdo do modal
    texto = (
        "Clique em 'Selecionar arquivo' ou 'Alterar arquivo' para carregar seu dataset.\n\n"
        "O arquivo deve conter colunas correspondentes a:\n\n"
        "• Gênero\n"
        "• Nome da música\n"
        "• Popularidade\n\n"
        "Após o processamento, selecione um gênero e veja o Top 10!"
    )

    tk.Label(
        modal,
        text=texto,
        bg="white",
        fg="black",
        justify="left",
        font=("Segoe UI", 10),
        wraplength=380
    ).pack(padx=20, pady=(5, 10))


    tk.Button(
        modal,
        text="Fechar",
        command=modal.destroy,
        bg="#0040FF",
        fg="white",
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        padx=6,
        pady=2
    ).pack(pady=(0, 10))
