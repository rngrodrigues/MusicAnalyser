import os
from tkinter import messagebox

def finalizar(root):
    if messagebox.askokcancel("Sair", "Tem certeza que deseja fechar o programa?"):
        try:
            root.destroy()
        except Exception:
            pass
        os._exit(0)
