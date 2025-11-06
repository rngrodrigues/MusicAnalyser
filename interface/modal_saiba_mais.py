import tkinter as tk

def abrir_saiba_mais(parent):
    modal = tk.Toplevel(parent)
    modal.title("Sobre o projeto")
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

    # Título centralizado
    tk.Label(
        modal,
        text="Music Analyser",
        bg="white",
        fg="#0040FF",
        font=("Segoe UI", 14, "bold")
    ).pack(pady=(15, 5))


    texto = (
        "O Music Analyser é um projeto acadêmico de Big Data, "
        "desenvolvido em Python, PySpark, Tkinter e Matplotlib."
        " Voltado para análise musicais.\n\n"
        "O objetivo é realizar a análise de grandes volumes de dados"
        "em diferentes formatos, permitindo visualizar "
        "informações musicais de forma interativa."
    )

    tk.Label(
        modal,
        text=texto,
        bg="white",
        fg="black",
        justify="left",
        font=("Segoe UI", 10),
        wraplength=380  # evita o corte do texto
    ).pack(padx=20, pady=10)

    # Botão de fechar
    tk.Button(
        modal,
        text="Fechar",
        command=modal.destroy,
        bg="#0040FF",
        fg="white",
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        padx=4,
        pady=2
    ).pack(pady=10)
