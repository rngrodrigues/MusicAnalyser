import os
from tkinter import messagebox
from core.spark_session import get_spark

def finalizar(root):

    if messagebox.askokcancel("Sair", "Tem certeza que deseja fechar o programa?"):
        try:
            spark = get_spark()
            spark.stop()
        except Exception:
            pass
        root.destroy()
        os._exit(0)
