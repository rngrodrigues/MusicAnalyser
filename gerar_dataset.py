import csv
import os
import random
import string
import sys
import time

# ===============================
# CONFIGURAÇÕES
# ===============================
ARQUIVO_SAIDA = "1bilhao.csv"
TOTAL_LINHAS = 1_000_000_000   # total de linhas
BATCH_PRINT = 100_000        # frequência de update da barra

GENEROS = [
    "Rock", "Pop", "Hip-Hop", "Jazz", "Blues",
    "Electronic", "Classical", "Reggae",
    "Country", "Metal"
]

TOP_POPULARIDADES = [90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100]  # valores únicos por gênero
TOP_HITS_POR_GENERO = len(TOP_POPULARIDADES)  # 10 top hits por gênero

# ===============================
# FUNÇÕES AUXILIARES
# ===============================
def gerar_nome_musica(i):
    """Gera um nome aleatório para a música"""
    return f"Track_{i}_{''.join(random.choices(string.ascii_letters, k=5))}"

def barra_progresso(atual, total, inicio):
    """Mostra barra de progresso no console"""
    progresso = atual / total
    largura = 40
    preenchido = int(largura * progresso)
    barra = "█" * preenchido + "-" * (largura - preenchido)
    percentual = progresso * 100

    tempo_decorrido = time.time() - inicio
    velocidade = atual / tempo_decorrido if tempo_decorrido > 0 else 0
    restantes = (total - atual) / velocidade if velocidade > 0 else 0

    sys.stdout.write(
        f"\r[{barra}] {percentual:6.2f}% | "
        f"{atual:,}/{total:,} linhas | "
        f"ETA: {int(restantes)}s"
    )
    sys.stdout.flush()

# ===============================
# GERAÇÃO DO CSV
# ===============================
def gerar_csv():
    inicio = time.time()
    linhas_geradas = 0
    id_musica = 1

    with open(ARQUIVO_SAIDA, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["genre", "track_name", "popularity"])

        # --------------------------
        # 1️⃣ Gerar os top hits obrigatórios (uma música por popularidade por gênero)
        # --------------------------
        for genero in GENEROS:
            for pop in TOP_POPULARIDADES:
                writer.writerow([
                    genero,
                    gerar_nome_musica(id_musica),
                    pop
                ])
                id_musica += 1
                linhas_geradas += 1
                if linhas_geradas % BATCH_PRINT == 0:
                    barra_progresso(linhas_geradas, TOTAL_LINHAS, inicio)

        # --------------------------
        # 2️⃣ Gerar o restante das linhas (popularidade 1 a 89, repetível)
        # --------------------------
        while linhas_geradas < TOTAL_LINHAS:
            genero = random.choice(GENEROS)
            popularidade = round(random.uniform(1, 89), 2)

            writer.writerow([
                genero,
                gerar_nome_musica(id_musica),
                popularidade
            ])
            id_musica += 1
            linhas_geradas += 1

            if linhas_geradas % BATCH_PRINT == 0:
                barra_progresso(linhas_geradas, TOTAL_LINHAS, inicio)

    barra_progresso(TOTAL_LINHAS, TOTAL_LINHAS, inicio)
    print("\n✅ CSV gerado com sucesso!")
    print(f"📁 Arquivo: {os.path.abspath(ARQUIVO_SAIDA)}")
    print(f"⏱️ Tempo total: {int(time.time() - inicio)}s")


# ===============================
# MAIN
# ===============================
if __name__ == "__main__":
    gerar_csv()
