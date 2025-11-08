import os
import pandas as pd
from tkinter import filedialog, messagebox
from matplotlib import pyplot as plt
from zipfile import ZipFile
import tempfile

def salvar_resultado(fig, top10_por_genero, genero):
    # Pergunta ao usuário o que salvar
    salvar_todos = messagebox.askyesno(
        "Salvar todos?",
        "Deseja salvar todos os gêneros?\n\n"
        "Sim → salva todos os gêneros.\n"
        "Não → salva apenas o gênero atual."
    )

    if salvar_todos:
        df_para_salvar = top10_por_genero
        genero_label = "todos_os_generos"
    else:
        df_para_salvar = top10_por_genero[top10_por_genero['genre'] == genero]
        genero_label = genero.replace(" ", "_")

    opcoes = [
        ("Gráfico PNG", "*.png"),
        ("Gráfico PDF", "*.pdf"),
        ("Dados CSV", "*.csv"),
        ("Planilha Excel", "*.xlsx")
    ]
    caminho = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=opcoes,
        title="Salvar resultados como...",
        initialfile=f"top10_{genero_label}"
    )

    if not caminho:
        messagebox.showinfo("Cancelado", "Nenhum arquivo foi salvo.")
        return

    ext = caminho.split(".")[-1].lower()

    try:
        if ext in ["png", "pdf"]:
            if salvar_todos:
                # Cria pasta temporária e salva todos os gráficos
                with tempfile.TemporaryDirectory() as tmpdir:
                    for g in sorted(top10_por_genero['genre'].unique()):
                        df = top10_por_genero[top10_por_genero['genre'] == g]
                        fig_temp, ax_temp = plt.subplots(figsize=(10, 6))
                        bars = ax_temp.barh(
                            df['track_name'], df['popularity'],
                            color='#4C8BFF', edgecolor='black', alpha=0.8
                        )
                        ax_temp.set_xlabel('Popularidade', fontsize=12)
                        ax_temp.set_ylabel('Música', fontsize=12)
                        ax_temp.set_title(f'Top 10 músicas mais populares de {g}', fontsize=14)
                        ax_temp.invert_yaxis()
                        for bar in bars:
                            ax_temp.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
                                         f"{int(bar.get_width())}", va='center', fontsize=9, fontweight='bold')
                        plt.tight_layout()
                        arquivo = os.path.join(tmpdir, f"top10_{g}.{ext}")
                        fig_temp.savefig(arquivo, format=ext, bbox_inches="tight", dpi=300)
                        plt.close(fig_temp)

                    # Compacta todos em ZIP
                    zip_path = caminho.replace(f".{ext}", ".zip")
                    with ZipFile(zip_path, "w") as zipf:
                        for file in os.listdir(tmpdir):
                            zipf.write(os.path.join(tmpdir, file), arcname=file)

                    messagebox.showinfo("Sucesso", f"Arquivos de todos os gêneros salvos em:\n{zip_path}")

            else:
                fig.savefig(caminho, format=ext, bbox_inches="tight", dpi=300)
                messagebox.showinfo("Sucesso", f"Gráfico salvo com sucesso:\n{caminho}")

        elif ext == "csv":
            df_para_salvar.to_csv(caminho, index=False, encoding="utf-8-sig")
            messagebox.showinfo("Sucesso", f"CSV salvo com sucesso:\n{caminho}")

        elif ext == "xlsx":
            if salvar_todos:
                with pd.ExcelWriter(caminho, engine='openpyxl') as writer:
                    for g in sorted(top10_por_genero['genre'].unique()):
                        df = top10_por_genero[top10_por_genero['genre'] == g]
                        df.to_excel(writer, sheet_name=g[:31], index=False)
            else:
                df_para_salvar.to_excel(caminho, index=False)
            messagebox.showinfo("Sucesso", f"Excel salvo com sucesso:\n{caminho}")

        else:
            messagebox.showerror("Erro", f"Formato não suportado: .{ext}")

    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível salvar o arquivo:\n{e}")
