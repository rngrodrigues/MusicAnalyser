import tkinter as tk

def abrir_modal(parent):
    modal = tk.Toplevel(parent)
    modal.title("Como usar o MusicAnalyser")
    largura, altura = 420, 260
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

    # Conteúdo do modal
    texto = (
        "Clique em 'Selecionar arquivo' para carregar seu dataset.\n\n"
        "O arquivo deve conter colunas como:\n"
        "- gênero (genre)\n"
        "- nome da música (track_name)\n"
        "- popularidade (popularity)\n\n"
        "Após carregar, selecione um gênero e veja o Top 10!"
    )

    tk.Label(modal, text=texto, bg="white", fg="black",
             justify="left", font=("Segoe UI", 10)).pack(padx=20, pady=20)

    tk.Button(
        modal, text="Fechar", command=modal.destroy,
        bg="#0040FF", fg="white", font=("Segoe UI", 10, "bold"),
        relief="flat", padx=10, pady=5
    ).pack(pady=10)
